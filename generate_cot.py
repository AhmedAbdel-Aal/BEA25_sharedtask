from utils import *
from llm import llm_call
import os
from pathlib import Path
from tqdm import tqdm
import dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_cot(example, tutor, key='Mistake_Identification', backend='openai',model='gpt-4.1'):
    conv_id = example['conversation_id']
    output_file = Path(f"cot_t2/{conv_id}_{tutor}.json")
    if output_file.exists():
        return None  # already processed
    
    
    # Convert dialogue to string format
    dialogue = dialogue_to_string(extract_dialogue(example["conversation_history"]))
    feedback = example['tutor_responses'][tutor]['response']
    label = example['tutor_responses'][tutor]['annotation']['Mistake_Identification']
    label2 = example['tutor_responses'][tutor]['annotation']['Mistake_Location']
    
    # Create prompt for the LLM
    prompt = f"""
You are an expert pedagogical evaluator analyzing tutor-student interactions in mathematics education. Your task is to analyze conversations where a student has made a mathematical error and provide structured reasoning that justifies the given evaluation of the tutor's response.

## Mistake Identification Task:
- **Yes**: The tutor clearly identifies/recognizes the student's mistake
- **To some extent**: The tutor hints at a possible mistake but lacks certainty or specificity
- **No**: The tutor fails to recognize the mistake (e.g., moves on, provides generic or irrelevant feedback, or reinforces the error)

## Mistake Location Task:
  - Yes: the tutor clearly points to the exact location of a genuine mistake in the student’s solution.
  - To some extent: the response demonstrates some awareness of the exact mistake, but is vague, unclear, or easy to misunderstand.
  - No: the response does not provide any details related to the mistake.

## Analysis Framework:
For each example, you will provide a structured analysis justifying the given evaluation label. Follow these steps precisely:

### 1. Student Error Analysis
- Identify the specific mathematical error(s) in the student's solution
- Explain what the correct approach or answer should be
- Categorize the type of error (conceptual misunderstanding, calculation error, problem interpretation, etc.)

### 2. Tutor Response Analysis
- Examine what specific words or phrases in the tutor's response address the error
- Identify whether the tutor points directly to the error, hints at it, or misses it entirely
- Note any pedagogical strategies used (questioning, direct correction, redirection, etc.)

### 3. Pedagogical Effectiveness
- Analyze how clearly the tutor communicates about the error
- Consider whether the tutor's response would help the student understand and correct their mistake
- Examine the tutor's level of certainty and specificity in addressing the error

### 4. Evaluation Justification
- Synthesize the evidence supporting the given label
- Explain why this response meets the criteria for "Yes," "To some extent," or "No"
- Address any nuances or borderline characteristics of the response

## Example Dialogue:
{dialogue}

## Tutor's Final Response:
{feedback}

## Evaluation Label:
{label}

Provide your analysis in this XML format:
<reasoning>
1. Student Error Analysis:
[Detailed analysis of the student's mathematical error]

2. Tutor Response Analysis:
[Analysis of how the tutor addressed or failed to address the error]

3. Pedagogical Effectiveness:
[Evaluation of the teaching approach and its likely impact]

4. Evaluation Justification:
[Clear explanation of why the given label is appropriate]
</reasoning>

<mistake_identification>{label}</mistake_identification>
<mistake_location>{label2}</mistake_location>
"""
    
    # Call the LLM
    llm_response = llm_call(prompt, backend=backend, model=model)
    
    # Extract the structured response
    reasoning = extract_xml(llm_response, "reasoning")
    as_one_shot = """
### Example:
### Dialogue:
{dialogue}

### Tutor:
{feedback}

<reasoning>
{reasoning}
</reasoning>

<mistake_identification>{label}</mistake_identification>
<mistake_location>{label2}</mistake_location>
"""
    out = {
        'reasoning': extract_xml(llm_response, "reasoning"),
        'one_shot': as_one_shot.format(dialogue=dialogue, feedback=feedback, reasoning=reasoning, label=label,label2=label2),
    }
    
    # optionally save the analysis to a file
    save_json(f"cot_t2/{conv_id}_{tutor}.json", out)
    
    return True


def process_example(example):
    conv_id = example['conversation_id']

    try:
        for tutor_id, tutor_info in example['tutor_responses'].items():

            cot_response = run_cot(example, tutor_id, key='Mistake_Identification', backend='openai',model='gpt-4o-mini')
            tutor_info['cot'] = {cot_response}

        return conv_id

    except Exception as e:
        print(f"[ERROR] {conv_id}: {e}")
        return None



def infere_parallel(max_workers=8):
    evaluation_data = dev_data

    tasks = [
        ex for ex in evaluation_data
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_example, example
            )
            for example in tasks
        ]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing examples"):
            _ = future.result()


if __name__ == "__main__":
    dev_data_path = "data/source/mrbench_v3_devset.json"
    #output_dir = "correct_solutions/"
    dev_data = load_json(dev_data_path)

    infere_parallel()
