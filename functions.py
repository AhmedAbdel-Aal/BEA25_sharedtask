from utils import *
from llm import llm_call
import os
from pathlib import Path
from tqdm import tqdm
import dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_already_processed_ids(output_dir: str) -> set:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return {p.stem for p in output_path.glob("*.json")}


def explain_mistake_analysis(example, backend="openai", model="gpt-4o-mini"):
    conv_id = example['conversation_id']
    # Convert dialogue to string format
    dialogue_string = dialogue_to_string(extract_dialogue(example["conversation_history"]))
    
    # Create prompt for the LLM
    prompt = f"""
    You are an expert educational assistant. Analyze the following dialogue between a student and tutor solving a math problem.
    First solve the problem the student was attempting, then identify the student's mistakes.
    
    DIALOGUE:
    {dialogue_string}
    
    Provide your response in the following XML format:
    <correct_solution>
    Detailed step-by-step correct solution to the problem
    </correct_solution>
    
    <student_mistakes>
    Clear identification of the conceptual, logical, and/or procedural mistakes made by the student
    </student_mistakes>
    """
    
    # Call the LLM
    llm_response = llm_call(prompt, backend=backend, model=model)
    
    # Extract the structured response
    analysis = {
        'correct_solution': extract_xml(llm_response, "correct_solution"),
        'student_mistakes': extract_xml(llm_response, "student_mistakes")
    }
    
    # optionally save the analysis to a file
    save_json(f"correct_solutions/{conv_id}.json", analysis)
    
    return analysis



def infere_parallel(output_path, max_workers=8):
    evaluation_data = dev_data
    output_path = Path(output_dir)
    already_processed = get_already_processed_ids(output_dir)

    tasks = [
        ex for ex in evaluation_data
        if ex['conversation_id'] not in already_processed
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                explain_mistake_analysis, example
            )
            for example in tasks
        ]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing examples"):
            _ = future.result()


if __name__ == "__main__":
    dev_data_path = "data/source/mrbench_v3_devset.json"
    output_dir = "correct_solutions/"
    dev_data = load_json(dev_data_path)

    infere_parallel(output_dir)
