# write python code to follect all json files in output folder into a list and write that in one json file

import os
from utils import load_json, save_json

def collect_json_files(output_dir: str) -> list:
    """
    Collect all JSON files in the output directory and return their contents as a list.
    """
    import os
    import json

    json_files = []
    for filename in os.listdir(output_dir):
        if filename.endswith('.json'):
            file_content = load_json(os.path.join(output_dir, filename))
            json_files.append(file_content)
    print(f"Collected {len(json_files)} JSON files from {output_dir}")
    return json_files

def write_collected_json(output_dir: str, submission_path: str):
    """
    Collect all JSON files in the output directory and write them into a single JSON file.
    """
    collected_data = collect_json_files(output_dir)
    
    # Write the collected data to a single JSON file
    save_json(os.path.join(submission_path), collected_data)


if __name__ == "__main__":
    output_dir = "experiment_dynamic_t1/output_test/"
    submission_path = "experiment_dynamic_t1/submission/predictions.json"
    
    write_collected_json(output_dir, submission_path)
    print(f"Collected JSON files have been written to {submission_path}")