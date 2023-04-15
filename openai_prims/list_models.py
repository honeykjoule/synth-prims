import json
import argparse
import openai
from load_api_key import load_api_key

def list_models(write_to_file=False):
    openai.api_key = load_api_key()
    models = openai.Model.list()
    if write_to_file:
        with open("openai_prims/models.json", "w") as f:
            json.dump(models, f)   
    return models

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List OpenAI models and write to a JSON file")
    parser.add_argument("--write-to-file", action="store_true", help="Write models to a JSON file")
    args=parser.parse_args()
    models = list_models(args.write_to_file)
    #print(models)