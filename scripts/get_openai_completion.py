import openai
from load_openai_api_key import load_openai_api_key
from load_data_path import load_data_path
from json_dump import json_dump

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

if __name__ == "__main__":
    response = get_openai_completion(prompt = "Why did the chicken cross the road", max_tokens = 100)