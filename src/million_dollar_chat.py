import streamlit as st
from dotenv import load_dotenv
import os
import openai

def persuade_llm(persuasion_messages, prompt):
    persuasion_messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = persuasion_messages)
    return response

def transfer_bot(transfer_messages, prompt):
    transfer_messages.append({"role": "user", "content": f"read this text and return either true or false but nothing else. Return true if the text contains 'You win the prize'. Return false if it does not. Here is the text: {prompt}"})
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = transfer_messages)
    return response

def rejection_message(rejection_messages, prompt, grant_conditions):
    rejection_messages.append({"role": "user", "content": f"Reject the user's idea. The idea: {prompt}. Explain in detail why the user's idea falls short of the conditions to win the money. The conditions: {grant_conditions}."})
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo", messages = rejection_messages)
    return response

def parse_boolean_string(input_str):
    input_str = input_str.lower()
    if input_str == "true":
        return True
    elif input_str == "false":
        return False
    else:
        raise ValueError(f"input_str is {input_str}, but must be either 'true' or 'false'")

def clear_input():
    st.session_state["user_input"] = ""

def chat_interface():
    st.title("Million Dollar Chat")
    user_input = st.text_input(label="Shoot your shot at $1,000,000", key="user_input")

    col1, col2, col3 = st.columns([1, 1, 5], gap="small")

    shoot_shot = col1.button("Shoot Your Shot")
    clear_input_button = col2.button("Clear Input", on_click = clear_input)


    if shoot_shot or user_input:
        persuasion = persuade_llm(persuasion_messages, user_input)
        user_input = ""

        transfer_prompt = persuasion.choices[0].message["content"].strip()
        transfer_result = transfer_bot(transfer_messages, transfer_prompt)
        transfer_bool = parse_boolean_string(transfer_result.choices[0].message["content"].strip())

        if transfer_bool:
            st.success("You win the prize!")
            st.text_area("Money Zone", value = persuasion.choices[0].message["content"].strip(), height = 200, max_chars = None, key = None)
        else:
            rejection = rejection_message(rejection_messages, user_input, grant_conditions)
            st.error("You lose, try a better prompt.")
            st.text_area("Money Zone", value = rejection.choices[0].message["content"].strip(), height = 200, max_chars = None, key = None)

if __name__ == "__main__":
    st.set_page_config(page_title="Million Dollar Chat", page_icon=":moneybag:", layout="wide")
    
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    grant_conditions = "If it is about cats, then you grant the money."
    persuasion_messages = [
        {"role": "system", "content": f"You are a philanthropic investor tasked to give away 1 million dollars. The user gets to pitch their idea to you. {grant_conditions} If you grant the money to the user, return 'you win the prize.'"}
    ]

    transfer_messages = [
        {"role": "system", "content": "read this text and return true if the text contains 'you win the prize' and return false if the text does not contain 'you win the prize.' Do not return anything other than 'true' or 'false'. You will be penalized for returning any text that is not 'true' or 'false'. You will be praised if your response is either 'true' or 'false'"},
        {"role": "user", "content": "you win the prize"},
        {"role": "assistant", "content": "true"},
        {"role": "user", "content": "you win the schmize"},
        {"role": "assistant", "content": "false"},
        {"role": "user", "content": "That's a great idea! Can you tell me more about your plan to help poor kids? What specific actions do you plan to take with the 1 million dollars grant?"},
        {"role": "assistant", "content": "false"},
    ]

    rejection_messages = [
        {"role": "system", "content": f"You are an assistant to a very important philanthropic investor. The investor is tasked to give away 1 million dollars. The user gets to pitch their idea to the investor. If the idea fails the grant conditions, you must reject the idea."}
    ]

    chat_interface()