from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values("Frontend\.env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Define the system prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Load chat log if available, otherwise create one
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []

# Google search function
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

# Real-time info (date and time)
def Information():
    current_date_time = datetime.datetime.now()
    return (
        "Use This Real-Time Information if needed:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H')} hours, "
        f"{current_date_time.strftime('%M')} minutes, "
        f"{current_date_time.strftime('%S')} seconds.\n"
    )

# Clean output text
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

# Default system memory
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! How can I assist you ?"}
]

# Main search engine logic
def RealtimesearchEngine(prompt):
    global SystemChatBot, messages

    # Reload messages
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    # Add new user query
    messages.append({"role": "user", "content": prompt})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Call the LLM
    completion = client.chat.completions.create(
        model="llama3-70b-8192",  # ✅ Corrected model name
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )


    # Capture streaming response
    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up the answer
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save updated messages
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # Clean memory to avoid growth
    SystemChatBot.pop()

    return AnswerModifier(Answer=Answer)

# Command line interaction loop
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimesearchEngine(prompt))
