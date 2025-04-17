import os
from pathlib import Path
from tqdm import tqdm
import dotenv

from utils import (
    load_json,
    save_json,
    extract_dialogue,
    dialogue_to_string,
    format_prompt,
    extract_xml,
)
from prompts import mistake_prompt_2, mistake_prompt
from llm import llm_call


dotenv.load_dotenv()

dev_data_path = "data/source/mrbench_v3_devset.json"
test_data_path = "data/source/mrbench_v3_testset.json"
output_dir = "experiment_1/output_dev/"

dev_data = load_json(dev_data_path)
test_data = load_json(test_data_path)


def get_already_processed_ids(output_dir: str) -> set:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)  # ensure directory exists
    return {p.stem for p in output_path.glob("*.json")}

def annotate_example(example: dict, prompt_template: str, backend: str = 'openai', model: str = "gpt-4o-mini") -> dict:
    dialogue_string = dialogue_to_string(extract_dialogue(example["conversation_history"]))

    for tutor_id, tutor_info in example['tutor_responses'].items():
        tutor_response = tutor_info['response']

        prompt = format_prompt(
            prompt_template,
            dialogue=dialogue_string,
            feedback=tutor_response
        )

        llm_response = llm_call(prompt, backend=backend, model=model)

        tutor_info['annotation'] = {
            'Mistake_Identification': extract_xml(llm_response, "mistake"),
            'Analysis': extract_xml(llm_response, "analysis"),
        }

    return example

def infere():
    dev_data = load_json(dev_data_path)
    evaluation_data = dev_data#[:50]
    already_processed = get_already_processed_ids(output_dir)

    for example in tqdm(evaluation_data, desc="Processing examples"):
        conv_id = example['conversation_id']
        if conv_id in already_processed:
            continue

        annotated = annotate_example(example, mistake_prompt)
        save_json(Path(output_dir) / f"{conv_id}.json", annotated)


if __name__ == "__main__":
    infere()