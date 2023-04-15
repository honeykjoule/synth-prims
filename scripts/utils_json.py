import os
import json
from utils_env import load_data_path

def json_dump(data, filename):
    data_path = load_data_path()
    filename = os.path.join(data_path, filename.encode('utf-8'))
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# if __name__ == "__main__":
#     json_dump("test", "test.json")