import openai
from load_openai_api_key import load_openai_api_key
from json_dump import json_dump

def get_openai_models(write_to_file=False):
    openai.api_key = load_openai_api_key()
    models = openai.Model.list()
    json_dump(models, "openai_models.json")
    return models

if __name__ == "__main__":
    get_openai_models()