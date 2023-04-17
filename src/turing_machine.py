import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def query_gpt4(state, user_input):
    messages = [
        {"role": "system", "content": f"Current state: {state}"}, 
        {"role": "user", "content": user_input}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.0
    )
    print(response.choices[0].message["content"].strip())
    return response.choices[0].message["content"].strip()

def main():
    state = []
    while True:
        user_input = input("Enter your command or 'quit' to exit: ")
        if user_input.lower() == "quit":
            break

        prompt = f"Given the current state {state}, perform the following command: {user_input}"
        result = query_gpt4(state=state, user_input=prompt)
        
        # Parse and update the state based on GPT-4's response
        state.append({"input": prompt, "response": result})

        print("Updated state:", state)

if __name__ == "__main__":
    main()
