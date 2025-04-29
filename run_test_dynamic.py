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

from prompt_base_t2 import prompt_base_t2

dev_data_path = "data/source/mrbench_v3_devset.json"
test_data_path = "data/source/mrbench_v3_testset.json"
output_dir = "experiment_dynamic_t2/output_test/"

dev_data = load_json(dev_data_path)
test_data = load_json(test_data_path)

test_nn = load_json('bert_neighbors_500/test_nearest_examples.json')

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

def get_nns_test(data, idx, tutor):
    # search data list for the example with the given index
    iid = idx + 'SEP' + tutor
    for example in data:
        if example['test_id'] == iid:
            return example


def get_few_shot_examples_test(example, tutor):
    eid = example['conversation_id']
    selected_startified_nn = []
    labels_list=['Yes', 'To some extent', 'No']
    
    label_groups = {label: 0 for label in labels_list}
    for tutor_id, tutor_info in example['tutor_responses'].items():
        if tutor_id != tutor:
            continue
        nns = get_nns_test(test_nn, eid, tutor_id)
        #print(f"there are {len(nns['nearest_examples'])} nearest examples")
        for nn in nns['nearest_examples'][1:]:
            nn_id = nn['id']
            nn_tutor = nn['label']
            nn_example = get_example_from_data(dev_data, nn_id)
            nn_label = nn_example['tutor_responses'][nn_tutor]['annotation']['Mistake_Location']
            
            if label_groups[nn_label] < 2:
                #path = f"./cot_t1/{nn_id}_{nn_tutor}.json"
                path = f"./cot_t2/{nn_id}_{nn_tutor}.json"
                print(f"Loading {path}")
                if not Path(path).exists():
                   from generate_cot import run_cot
                   print('ah will do the cot')
                   run_cot(nn_example, nn_tutor, model='gpt-4o-mini')
                cot = load_json(path)
                selected_startified_nn.append(cot['reasoning'])
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
    few_shot_examples = get_few_shot_examples_test(example, tutor_id)
    if few_shot_examples is None:
        return None
    few_shot_text = "\n\n".join(few_shot_examples)

    return few_shot_text

def process_example(example, base_prompt_template, backend, model, output_path):
    conv_id = example['conversation_id']
    output_file = output_path / f"{conv_id}.json"
    
    if output_file.exists():
        return None  # already processed
    flag  = False
    try:
        dialogue_string = dialogue_to_string(extract_dialogue(example["conversation_history"]))
        for tutor_id, tutor_info in example['tutor_responses'].items():
            # Only process if tutor_response exists
            if 'response' not in tutor_info:
                continue
                
            tutor_response = tutor_info['response']
            
            # Create dynamic prompt based on this specific example and tutor
            few_shot_text = get_few_shot_text(example, tutor_id)
            if few_shot_text is None:
                print(f"Few-shot examples not found for {conv_id} and {tutor_id}")
                continue
            # The placeholders in prompt_base_t1 are {dialogue}, {feedback}, and {few_shot_examples}
            # The {few_shot_examples} is already replaced in create_dynamic_prompt
            prompt = base_prompt_template.format(
                few_shot_examples=few_shot_text,
                dialogue=dialogue_string,
                feedback=tutor_response
            )
            #print(f"Prompt for {conv_id}:\n{prompt}")
    
            # Call LLM with the dynamic prompt
            llm_response = llm_call(prompt, backend=backend, model=model)
            
            # Extract and save results
            tutor_info['annotation'] = {
                'Mistake_Identification': extract_xml(llm_response, "mistake_identification"),
                'Mistake_Location': extract_xml(llm_response, "mistake_location"),
                'Analysis': extract_xml(llm_response, "analysis"),
                'initial_prompt': prompt,
            }
            flag = True
        
        if flag:
            save_json(output_file, example)
        return conv_id
    
    except Exception as e:
        print(f"[ERROR] {conv_id}: {e}")
        return None

def infere_parallel(base_prompt_template, backend="openai", model="gpt-4o", max_workers=8):
    evaluation_data = test_data
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

def infer_sequential(base_prompt_template, backend="openai", model="gpt-4o"):
    """
    Process examples sequentially (one after another) instead of in parallel
    """
    evaluation_data = test_data
    output_path = Path(output_dir)
    already_processed = get_already_processed_ids(output_dir)
    
    tasks = [
        ex for ex in evaluation_data
        if ex['conversation_id'] not in already_processed
    ]
    
    print(f"Processing {len(tasks)} examples sequentially...")
    
    for example in tqdm(tasks, desc="Processing examples"):
        try:
            result = process_example(example, base_prompt_template, backend, model, output_path)
            if result:
                print(f"Processed example: {result}")
        except Exception as e:
            print(f"Error processing example {example['conversation_id']}: {e}")
            continue
    
    print("Sequential processing complete!")

#if __name__ == "__main__":
    # Use sequential processing instead of parallel
#    infer_sequential(prompt_base_t2)

if __name__ == "__main__":
    # Use the prompt base from prompts.py which already has the {few_shot_examples} placeholder
    infere_parallel(prompt_base_t2)