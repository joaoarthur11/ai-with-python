import os
import openai
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv()) 

client = openai.Client()

def send_and_append_message(messages, model="gpt-4o", max_tokens=300, temperature=0):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )

        print("\n🤖 Assistente: ", end="", flush=True)

        full_response = ""
        for stream in response:
            if stream.choices[0].delta.content:
                text = stream.choices[0].delta.content
                full_response += text
                print(text, end="", flush=True)

        print()

        messages.append({"role": "assistant", "content": full_response})
        return messages
    
    except Exception as error:
        print("\nErro ao chamar a API:", error)
        return messages



def start_chat():
    messages = []
    print("💬 Chat iniciado! (Digite 'sair' para encerrar)\n")

    while True:
        user_input = input("👤 Você: ")
        if user_input.lower() == "sair":
            print("\n🔚 Chat encerrado!")
            break
        messages.append({"role": "user", "content": user_input})
        messages = send_and_append_message(messages)