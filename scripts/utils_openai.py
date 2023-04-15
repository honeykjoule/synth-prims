import openai
from utils_env import load_openai_api_key, load_data_path
from utils_json import json_dump

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