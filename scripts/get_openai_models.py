import os
import json
import argparse
import openai
from load_openai_api_key import load_openai_api_key
from load_data_path import load_data_path

def list_models(write_to_file=False):
    openai.api_key = load_openai_api_key()
    models = openai.Model.list()
    if write_to_file:
        data_path = load_data_path()
        output_file = os.path.join(data_path, b"openai_models.json")
        with open(output_file, "w") as f:
            json.dump(models, f, indent=4)   
    return models

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List OpenAI models and write to a JSON file")
    parser.add_argument("--write-to-file", action="store_true", help="Write models to a JSON file")
    args=parser.parse_args()
    list_models(args.write_to_file)
    #print(models)