import os
import random
from pathlib import Path
from huggingface_hub import snapshot_download
from bitaudit.utils.const import *
import pandas as pd
import bittensor as bt


def download_dataset(download_path):
    # Specify your desired destination path
    repo_id = HUGGINGFACE_REPO_ID
    os.makedirs(download_path, exist_ok=True)
    # Download the dataset to the specified path
    hf_token = os.environ.get("HF_TOKEN")
    snapshot_download(repo_id=repo_id, local_dir=download_path,
                      repo_type="dataset", token=hf_token, force_download=False)


def generate_random_path(dataset_path):
    random_subset = random.choice(VALIDATION_SUBSET)
    random_category = random.choice(VULNERABILITY_CATEGORY)
    directory_path = os.path.join(dataset_path, f"{random_subset}/{random_category}")

    # Get a list of all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # Check if the directory is not empty
    if files:
        # Choose a random file from the list
        random_file = random.choice(files)
        bt.logging.info("Randomly chosen file:", random_file)
    else:
        bt.logging.info("Directory is empty.")

    smart_contract_path = os.path.join(dataset_path, f"{random_subset}/{random_category}/{random_file}")
    return smart_contract_path


def lowercase_dict(input_dict):
    processed_dict = {}
    for key, value in input_dict.items():
        # Stripping and lowercasing keys
        processed_key = key.strip().lower()

        # Stripping and lowercasing values
        if isinstance(value, str):
            processed_value = value.strip().lower()
        else:
            processed_value = value

        processed_dict[processed_key] = processed_value

    return processed_dict


def generate_labels(dataset_path, file_path):
    # Load the CSV file
    df = pd.read_csv(os.path.join(dataset_path, "output.csv"))

    # Filter the rows based on file number
    filtered_df = df[df['file'] == int(file_path.split('.')[0].split('/')[-1]) and df['subdataset'] == file_path.split('.')[0].split('/')[-3]]

    # Check if 'ground truth' has a single unique value
    unique_ground_truth_values = filtered_df[filtered_df['ground truth'] == 1]
    label = {}
    if len(unique_ground_truth_values) > 0:
    # Add only the rows with a single unique value to the result list
        for index, row in unique_ground_truth_values.iterrows():
            label.update({row['contract']: row['error_type']})
    return label