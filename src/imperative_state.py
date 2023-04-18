import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chat_completion(messages, prompt):
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message["content"].strip()

def update_state(state, imperative):
    prompt = f"Given the current state '{state[-1]['content']}' and the imperative '{imperative[-1]['content']}', return the next state."
    new_state_content = get_chat_completion(state + imperative, prompt)
    new_state = state.copy()
    new_state.append({"role": "assistant", "content": new_state_content})
    return new_state

def update_imperative(state):
    prompt = f"Given the current state '{state[-1]['content']}', return the next imperative."
    new_imperative_content = get_chat_completion(state, prompt)
    new_imperative = [{"role": "assistant", "content": new_imperative_content}]
    return new_imperative

if __name__ == "__main__":

    imperative = [
        {"role": "system", 
        "content": "Your instructions are to update the imperative as best you can based on the user's input."},
        {"role": "user",
        "content": "Develop a task list to simulate a Turing complete machine."}
    ]

    state = [
        {"role": "system",
        "content": "Your instructions are to update the state as best you can based on the user's input."},
    ]

    max_iterations = 2
    iteration_counter = 0
    
    while iteration_counter < max_iterations:

        # completion = get_chat_completion(imperative, imperative[-1]["content"])
        # state = update_state(completion)
        state = update_state(state, imperative)
        imperative = update_imperative(state)

        iteration_counter += 1

        print(f"Iteration {iteration_counter}:")
        print("Updated state:", state[-1]["content"])
        print("Updated imperative:", imperative[-1]["content"])