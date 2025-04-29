import os
from pathlib import Path
from tqdm import tqdm
import dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import (
    load_json,
    save_json,
    extract_dialogue,
    dialogue_to_string,
    format_prompt,
    extract_xml,
)
from llm import llm_call
dotenv.load_dotenv()

from prompt_base_t1 import prompt_base_t1

dev_data_path = "data/source/mrbench_v3_devset.json"
output_dir = "experiment_dynamic_t1/output_dev/"

dev_data = load_json(dev_data_path)
dev_nn = load_json("/Users/ahmed/Desktop/BEA25_sharedtask/bert_neighbors_500/dev_nearest_examples.json")

def get_example_from_data(data, idx):
    # search data list for the example with the given index
    for example in data:
        if example['conversation_id'] == idx:
            return example
        
def get_nns_dev(data, idx, tutor):
    # search data list for the example with the given index
    iid = idx + 'SEP' + tutor
    for example in data:
        if example['dev_id'] == iid:
            return example

def get_few_shot_examples_dev(example, tutor):
    eid = example['conversation_id']
    selected_startified_nn = []
    labels_list=['Yes', 'To some extent', 'No']
    label_groups = {label: 0 for label in labels_list}
    
    for tutor_id, tutor_info in example['tutor_responses'].items():
        if tutor_id != tutor:
            continue
        
        nns = get_nns_dev(dev_nn, eid, tutor_id)
        #print(f"there are {len(nns['nearest_examples'])} nearest examples")
        
        for nn in nns['nearest_examples'][1:]:
            nn_id, nn_tutor = nn['id'].split('SEP')
            nn_example = get_example_from_data(dev_data, nn_id)
            nn_label = nn_example['tutor_responses'][nn_tutor]['annotation']['Mistake_Identification']
            
            if label_groups[nn_label] < 3:
                path = f"./cot_t1/{nn['id'].replace('SEP', '_')}.json"
                cot = load_json(path)
                selected_startified_nn.append(cot['one_shot'])
                label_groups[nn_label] += 1
                
    return selected_startified_nn

def get_few_shot_examples_dev_stratified(example, tutor):
    eid = example['conversation_id']
    selected_startified_nn = []
    labels_list=['Yes', 'To some extent', 'No']
    
    # Set different thresholds for each label
    label_thresholds = {
        'Yes': 2,           # 1 less than before (was 3)
        'To some extent': 5, # 2 more than before (was 3)
        'No': 2             # 1 less than before (was 3)
    }
    
    # Initialize counters
    label_groups = {label: 0 for label in labels_list}
    
    for tutor_id, tutor_info in example['tutor_responses'].items():
        if tutor_id != tutor:
            continue
        
        nns = get_nns_dev(dev_nn, eid, tutor_id)
        #print(f"there are {len(nns['nearest_examples'])} nearest examples")
        
        for nn in nns['nearest_examples'][1:]:
            nn_id, nn_tutor = nn['id'].split('SEP')
            nn_example = get_example_from_data(dev_data, nn_id)
            nn_label = nn_example['tutor_responses'][nn_tutor]['annotation']['Mistake_Identification']
            
            # Check against the threshold for this specific label
            if label_groups[nn_label] < label_thresholds[nn_label]:
                path = f"./cot_t1/{nn['id'].replace('SEP', '_')}.json"
                cot = load_json(path)
                selected_startified_nn.append(cot['one_shot'])
                label_groups[nn_label] += 1
                
    return selected_startified_nn
def get_already_processed_ids(output_dir: str) -> set:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return {p.stem for p in output_path.glob("*.json")}

def get_few_shot_text(example, tutor_id):
    """
    Create a prompt dynamically by getting few-shot examples
    and formatting them into the prompt template
    """
    few_shot_examples = get_few_shot_examples_dev(example, tutor_id)
    few_shot_text = "\n\n".join(few_shot_examples)

    return few_shot_text

def process_example(example, base_prompt_template, backend, model, output_path):
    conv_id = example['conversation_id']
    output_file = output_path / f"{conv_id}.json"
    
    if output_file.exists():
        return None  # already processed
    
    try:
        dialogue_string = dialogue_to_string(extract_dialogue(example["conversation_history"]))
        for tutor_id, tutor_info in example['tutor_responses'].items():
            # Only process if tutor_response exists
            if 'response' not in tutor_info:
                continue
                
            tutor_response = tutor_info['response']
            
            # Create dynamic prompt based on this specific example and tutor
            few_shot_text = get_few_shot_text(example, tutor_id)
            # The placeholders in prompt_base_t1 are {dialogue}, {feedback}, and {few_shot_examples}
            # The {few_shot_examples} is already replaced in create_dynamic_prompt
            prompt = base_prompt_template.format(
                few_shot_examples=few_shot_text,
                dialogue=dialogue_string,
                feedback=tutor_response
            )
            
            # Call LLM with the dynamic prompt
            llm_response = llm_call(prompt, backend=backend, model=model)
            
            # Extract and save results
            tutor_info['annotation'] = {
                'Mistake_Identification': extract_xml(llm_response, "mistake_identification"),
                'Analysis': extract_xml(llm_response, "analysis"),
                'initial_prompt': prompt,
            }
        
        save_json(output_file, example)
        return conv_id
    
    except Exception as e:
        print(f"[ERROR] {conv_id}: {e}")
        return None

def infere_parallel(base_prompt_template, backend="qwen", model="gpt-4o-mini", max_workers=8):
    evaluation_data = dev_data[0:30]
    output_path = Path(output_dir)
    already_processed = get_already_processed_ids(output_dir)
    
    tasks = [
        ex for ex in evaluation_data
        if ex['conversation_id'] not in already_processed
    ]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_example, example, base_prompt_template, backend, model, output_path
            )
            for example in tasks
        ]
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing examples"):
            _ = future.result()


# Add a reflection prompt template
reflection_prompt_template = """
You previously analyzed a dialogue and provided an assessment about mistake identification.

Original dialogue: {dialogue}
Tutor feedback: {feedback}
Your initial analysis: {initial_analysis}

Now, please reflect on your analysis:
1. Did you correctly identify whether the tutor pointed out a mistake? 
2. Did you consider all relevant evidence from the dialogue and feedback?
3. Is your analysis consistent with the examples you've seen?

Please review and verify your answer, then provide your final assessment:

<reflection>
[Your reflection on your initial analysis, considering the evidence carefully]
</reflection>

<revised_mistake_identification>Yes|No|To some extent</revised_mistake_identification>

<revised_analysis>
[Your revised analysis, if needed]
</revised_analysis>
"""

def process_example_with_reflection(example, base_prompt_template, backend, model, output_path):
    conv_id = example['conversation_id']
    output_file = output_path / f"{conv_id}.json"
    
    if output_file.exists():
        return None  # already processed
    
    try:
        dialogue_string = dialogue_to_string(extract_dialogue(example["conversation_history"]))
        for tutor_id, tutor_info in example['tutor_responses'].items():
            # Only process if tutor_response exists
            if 'response' not in tutor_info:
                continue
                
            tutor_response = tutor_info['response']
            
            # Create dynamic prompt based on this specific example and tutor
            few_shot_text = get_few_shot_text(example, tutor_id)
            # The placeholders in prompt_base_t1 are {dialogue}, {feedback}, and {few_shot_examples}
            prompt = base_prompt_template.format(
                few_shot_examples=few_shot_text,
                dialogue=dialogue_string,
                feedback=tutor_response
            )
            if '### Example: Probing Question (Vague Hint)' in prompt:
                print('a7aaaaaa')
                return
            
            # Initial LLM call
            initial_response = llm_call(prompt, backend=backend, model=model)
            
            # Extract initial analysis
            initial_mistake_id = extract_xml(initial_response, "mistake_identification")
            initial_analysis = extract_xml(initial_response, "analysis")
            
            # Create reflection prompt
            reflection_prompt = reflection_prompt_template.format(
                dialogue=dialogue_string,
                feedback=tutor_response,
                initial_analysis=initial_response
            )
            
            # Call LLM for reflection
            reflection_response = llm_call(reflection_prompt, backend=backend, model=model)
            
            # Extract revised assessment
            reflection_text = extract_xml(reflection_response, "reflection")
            revised_mistake_id = extract_xml(reflection_response, "revised_mistake_identification")
            revised_analysis = extract_xml(reflection_response, "revised_analysis")
            
            # If no revision was made, keep the original
            final_mistake_id = revised_mistake_id if revised_mistake_id else initial_mistake_id
            final_analysis = revised_analysis if revised_analysis else initial_analysis
            
            # Save results
            tutor_info['annotation'] = {
                'Mistake_Identification': final_mistake_id,
                'Analysis': final_analysis,
                'Reflection': reflection_text,
                'Initial_Mistake_Identification': initial_mistake_id,
                'Initial_Analysis': initial_analysis,
                'initial_prompt': prompt,
                'reflection_prompt': reflection_prompt,
            }
        
        save_json(output_file, example)
        return conv_id
    
    except Exception as e:
        print(f"[ERROR] {conv_id}: {e}")
        return None

def infere_parallel_with_reflection(base_prompt_template, backend="openai", model="gpt-4o-mini", max_workers=8):
    evaluation_data = dev_data[0:1]
    output_path = Path(output_dir)
    already_processed = get_already_processed_ids(output_dir)
    
    tasks = [
        ex for ex in evaluation_data
        if ex['conversation_id'] not in already_processed
    ]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_example_with_reflection, example, base_prompt_template, backend, model, output_path
            )
            for example in tasks
        ]
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing examples"):
            _ = future.result()

#if __name__ == "__main__":
    # Use the reflection-enabled pipeline
#    infere_parallel_with_reflection(prompt_base_t1)


if __name__ == "__main__":
    # Use the prompt base from prompts.py which already has the {few_shot_examples} placeholder
    infere_parallel(prompt_base_t1)