import os
from dotenv import load_dotenv
import openai

load_dotenv()

def load_api_key():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    return OPENAI_API_KEY

if __name__ == "__main__":
    load_api_key()
    print(load_api_key())