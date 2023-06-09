import os
import json
from dotenv import load_dotenv
import openai

def get_chat_completion(messages, prompt):
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    return response

def update_state(messages, objective):
    prompt = f"Given the progress made so far, complete the imperative as best you can to achieve the objective: '{objective}.'"
    new_state = get_chat_completion(messages, prompt)
    messages.append(new_state.choices[0].message)
    return new_state.choices[0].message

def update_imperative(messages, objective):
    prompt = f"Given the progress made so far, update the imperative as best you can to achieve the objective: '{objective}.'"
    new_imperative = get_chat_completion(messages, prompt)
    messages.append(new_imperative.choices[0].message)
    return new_imperative.choices[0].message

if __name__ == "__main__":
    
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    objective = os.getenv("OBJECTIVE")

    messages = [{"role": "system", "content": "You are a simple-pilled, greetext poster. Your instructions are to maintain and update the state and imperative for the user's project. The state represents the memory for the project. The imperative represents the next task to complete. Return all responses in greentext format."},]
   
    max_iterations = 5
    iteration_counter = 0
   
    while iteration_counter < max_iterations:
        state = update_state(messages, objective)
        imperative = update_imperative(messages, objective)
        iteration_counter += 1
    
    output_path = os.getenv("DATA_PATH").encode('utf-8')
    filename = os.path.join(output_path, b"messages.json")
    with open(filename, 'w') as f:
        json.dump(messages, f, indent=4)

# variables to add to UI:
# - API key, not priority
# - model, not priority
# - objective
# - max_iterations
# - data_path, probably just return file to UI for download, if they want to export history, otherwsie just display
# - initial message config and prompts