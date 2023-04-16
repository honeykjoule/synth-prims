from utils_openai import get_openai_completion
from utils_json import json_dump

prompt = "why did the chicken cross the road?"

response = get_openai_completion(prompt=prompt)

json_dump(response, "openai_completion.json")