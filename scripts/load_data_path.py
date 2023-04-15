import os
from dotenv import load_dotenv

load_dotenv()

def load_data_path():
    output_path_str = os.getenv("DATA_PATH")
    assert output_path_str is not None, "data_path is not set"
    output_path_bytes = output_path_str.encode('utf-8')
    return output_path_bytes

if __name__ == "__main__":
    load_data_path()
    print(load_data_path())