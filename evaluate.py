from prepare_output_file import collect_json_files
from utils import load_json, save_json
from tqdm import tqdm
import dotenv

import argparse

dotenv.load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate the model's predictions.")
    parser.add_argument("--experiment", "-e", type=str, required=True, help="experiment number.")
    return parser.parse_args()
args = parse_args()
experiment_number = args.experiment


dev_predictions_path = f"experiment_{experiment_number}/output_dev/"
dev_predictions = collect_json_files(dev_predictions_path)
dev_truth = load_json("data/source/mrbench_v3_devset.json")

print(f"The evaluation fromt the experiment in {dev_predictions_path} is loaded")
print("Number of predictions:", len(dev_predictions))

from sklearn.metrics import f1_score

def evaluate_mistake_identification_f1_multiclass(gold_data, pred_data, mode='strict', average="macro"):
    y_true = []
    y_pred = []

    label_mapping = {
        "yes": 0,
        "to some extent": 1,
        "no": 2
    }

    if mode != 'strict':
        label_mapping = {
        "yes": 0,
        "to some extent": 0,
        "no":1
        }


    pred_lookup = {item['conversation_id']: item for item in pred_data}

    for gold_item in gold_data:
        conv_id = gold_item['conversation_id']
        if conv_id not in pred_lookup:
            continue

        pred_item = pred_lookup[conv_id]

        for model_name, gold_response in gold_item['tutor_responses'].items():
            if model_name not in pred_item['tutor_responses']:
                continue

            pred_response = pred_item['tutor_responses'][model_name]

            gold_label = gold_response['annotation']['Mistake_Identification'].strip().lower()
            pred_label = pred_response['annotation']['Mistake_Identification'].strip().lower()

            if gold_label in label_mapping and pred_label in label_mapping:
                y_true.append(label_mapping[gold_label])
                y_pred.append(label_mapping[pred_label])

    if not y_true:
        print("No matching predictions found.")
        return 0.0

    return f1_score(y_true, y_pred, average=average), y_true, y_pred

f1, y_true, y_pred = evaluate_mistake_identification_f1_multiclass(dev_truth, dev_predictions, average="macro")
print("Strict F1 Score (macro):", f1)

f1, y_true, y_pred = evaluate_mistake_identification_f1_multiclass(dev_truth, dev_predictions, mode = 'lentient', average="macro")
print("Lentient F1 Score (macro):", f1)
