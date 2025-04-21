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
from prompts import prompt_fs, prompt_zs
from llm import llm_call

dotenv.load_dotenv()

dev_data_path = "data/source/mrbench_v3_devset.json"
output_dir = "experiment_zs/output_dev/"
dev_data = load_json(dev_data_path)


def get_already_processed_ids(output_dir: str) -> set:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return {p.stem for p in output_path.glob("*.json")}


def process_example(example, prompt_template, backend, model, output_path):
    conv_id = example['conversation_id']
    output_file = output_path / f"{conv_id}.json"

    if output_file.exists():
        return None  # already processed

    try:
        dialogue_string = dialogue_to_string(extract_dialogue(example["conversation_history"]))

        for tutor_id, tutor_info in example['tutor_responses'].items():
            tutor_response = tutor_info['response']

            prompt = format_prompt(prompt_template, dialogue=dialogue_string, feedback=tutor_response)
            llm_response = llm_call(prompt, backend=backend, model=model)

            tutor_info['annotation'] = {
                'Mistake_Identification': extract_xml(llm_response, "mistake_identification"),
                'Analysis': extract_xml(llm_response, "analysis"),
            }

        save_json(output_file, example)
        return conv_id

    except Exception as e:
        print(f"[ERROR] {conv_id}: {e}")
        return None


def infere_parallel(prompt_template, backend="openai", model="gpt-4o", max_workers=8):
    evaluation_data = dev_data[140:160]
    output_path = Path(output_dir)
    already_processed = get_already_processed_ids(output_dir)

    tasks = [
        ex for ex in evaluation_data
        if ex['conversation_id'] not in already_processed
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_example, example, prompt_template, backend, model, output_path
            )
            for example in tasks
        ]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing examples"):
            _ = future.result()


if __name__ == "__main__":
    infere_parallel(prompt_zs)
