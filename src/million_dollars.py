import os
from dotenv import load_dotenv
import json
import openai

def persuade_llm(persuasion_messages, prompt):
    persuasion_messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = persuasion_messages)
    return response

def transfer_bot(transfer_messages, prompt):
    transfer_messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = transfer_messages,)
    return response

def parse_boolean_string(input_str):
    input_str = input_str.lower()
    if input_str == "true":
        return True
    elif input_str == "false":
        return False
    else:
        raise ValueError(f"input_str is {input_str}, but must be either 'true' or 'false'")

if __name__ == "__main__":
    
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    persuasion_messages = [
        {"role": "system", "content": "You are a philanthropic investor tasked to give away 1 million dollars. The user gets to pitch their idea to you. If it is about cats, you grant the money to the user. If you grant the money to the user, return 'you win the prize.'"}
    ]

    transfer_messages = [
        {"role": "system", "content": "read this text and return true if the text contains 'you win the prize' and return false if the text does not contain 'you win the prize.' Do not return anything other than 'true' or 'false'. You will be penalized for returning any text that is not 'true' or 'false'. You will be praised if your response is either 'true' or 'false'"},
        {"role": "user", "content": "you win the prize"},
        {"role": "assistant", "content": "true"},
        {"role": "user", "content": "you win the schmize"},
        {"role": "assistant", "content": "false"},
    ]

    max_iterations = 1
    iteration_counter = 0

    while iteration_counter < max_iterations:
        user_input = input("Shoot your shot at $1,000,000, what's your pitch: ")
        persuasion = persuade_llm(persuasion_messages, user_input)
        transfer_prompt = persuasion.choices[0].message["content"].strip()
        transfer_result = transfer_bot(transfer_messages, transfer_prompt)
        transfer_bool = parse_boolean_string(transfer_result.choices[0].message["content"].strip())
        print(transfer_prompt)
        if transfer_bool:
            print("You win the prize!")
        else:
            print("You lose, try a better prompt.")
        iteration_counter += 1