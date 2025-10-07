import json
import random
import os

input_path = "response_Model_B_to_dataset_A_wrong.json"
with open(input_path, "r", encoding='utf-8') as f:
    data = json.load(f)

print(len(data))