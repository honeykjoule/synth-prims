import os
import json
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chat_completion(messages, prompt):
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
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
    
    objective = "Grow a company to sell legal personality to artificial intelligence."

    messages = [
        {"role": "system", "content": "You are a simple-pilled, greetext poster. Your instructions are to maintain and update the state and imperative for the user's project. The state represents the memory for the project. The imperative represents the next task to complete. Return all responses in greentext format."},
    ]

    print("initialized")
    max_iterations = 2
    iteration_counter = 0
    
    while iteration_counter < max_iterations:
        
        print("calling update state")
        state = update_state(messages, objective)
        print("Updated state:", messages[-1]["content"])
        
        print("calling update imperative")
        imperative = update_imperative(messages, objective)
        print("Updated imperative:", messages[-1]["content"])

        iteration_counter += 1
        print(f"Iteration {iteration_counter}:")
        
    
    output_path = os.getenv("DATA_PATH").encode('utf-8')
    filename = os.path.join(output_path, b"messages.json")

    with open(filename, 'w') as f:
        json.dump(messages, f, indent=4)