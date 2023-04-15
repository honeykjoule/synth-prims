import os
from dotenv import load_dotenv

load_dotenv()

def load_openai_api_key():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    assert OPENAI_API_KEY is not None, "OPENAI_API_KEY is not set"
    return OPENAI_API_KEY

if __name__ == "__main__":
    load_openai_api_key()