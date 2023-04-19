import os
from dotenv import load_dotenv
import json
import openai


# env
def load_data_path():
    output_path_str = os.getenv("DATA_PATH")
    assert output_path_str is not None, "data_path is not set"
    output_path_bytes = output_path_str.encode('utf-8')
    return output_path_bytes

def load_openai_api_key():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    assert OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set"
    return OPENAI_API_KEY

# json
def json_dump(data, filename):
    data_path = load_data_path()
    filename = os.path.join(data_path, filename.encode('utf-8'))
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def json_load(filename):
    data_path = load_data_path()
    filename = os.path.join(data_path, filename.encode('utf-8'))
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# openai
def get_openai_models():
    openai.api_key = load_openai_api_key()
    models = openai.Model.list()
    json_dump(models, "openai_models.json")
    return models

def get_openai_completion(
    model = "text-davinci-003",
    prompt = "<|endoftext|>",
    suffix = None,
    max_tokens = 100,
    temperature=1.0,
    top_p = 1.0,
    n = 1,
    stream = False,
    logprobs = None,
    echo = False,
    stop = None,
    presence_penalty = 0.0,
    frequency_penalty = 0.0,
    best_of = 1,
    # logit_bias = None,
    # user = None
):
    openai.api_key = load_openai_api_key()
    data_path = load_data_path()
    response = openai.Completion.create(
        model = model,
        prompt = prompt,
        suffix = suffix,
        max_tokens = max_tokens,
        temperature = temperature,
        top_p = top_p,
        n = n,
        stream = stream,
        logprobs = logprobs,
        echo = echo,
        stop = stop,
        presence_penalty = presence_penalty,
        frequency_penalty = frequency_penalty,
        best_of = best_of,
        # logit_bias = logit_bias,
        # user = user
    )
    # json_dump(response, "openai_completion.json")
    return response

def get_openai_chat_completon(
    model = "gpt-3.5-turbo",
    messages = []
):
    openai.api_key = load_openai_api_key()
    data_path = load_data_path()
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages
    )
    json_dump(response, "openai_chat_completion.json")
    return response