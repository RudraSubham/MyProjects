from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# Load environment variables
env_vars = dotenv_values("Frontend/.env")

# Get required variables
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "AI Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Short and optimized system prompt
System = f"""You are {Assistantname}, a smart and helpful AI chatbot. 
Always reply in English. Don't give time unless asked. 
Be concise. Never mention your training data or provide notes."""

SystemChatBot = [
    {"role": "system", "content": System}
]

def load_chat_log(file_path):
    try:
        with open(file_path, "r") as f:
            return load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading chat log: {e}")
        return []

def save_chat_log(file_path, messages):
    try:
        with open(file_path, "w") as f:
            dump(messages, f, indent=4)
    except Exception as e:
        print(f"Error saving chat log: {e}")

def get_realtime_information():
    now = datetime.datetime.now()
    return (
        f"Real-time info:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')}:{now.strftime('%M')}:{now.strftime('%S')}\n"
    )

def modify_answer(answer):
    lines = answer.split('\n')
    non_empty = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty)

def chatbot(query):
    if not isinstance(query, str):
        raise ValueError("Input must be a string.")

    file_path = "Data/ChatLog.json"
    history = load_chat_log(file_path)[-4:]  # Trimmed to last 4 interactions
    history.append({"role": "user", "content": query})

    # Include real-time info only if relevant
    realtime_info = []
    if any(kw in query.lower() for kw in ["time", "date", "day", "month", "year"]):
        realtime_info = [{"role": "system", "content": get_realtime_information()}]

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + realtime_info + history,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        answer = ""
        for chunk in completion:
            if hasattr(chunk, "choices") and chunk.choices:
                answer += chunk.choices[0].delta.content or ""

        answer = answer.strip()
        history.append({"role": "assistant", "content": answer})
        save_chat_log(file_path, history)

        return modify_answer(answer)

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Questions: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        try:
            answer = chatbot(user_input)
            if answer:
                print(answer)
        except Exception as e:
            print(f"Error: {e}")
