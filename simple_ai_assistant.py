
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv() # Load environment variables from .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []
while True:
    user_input = input("\n You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    print(f"\n Assistant: {response.choices[0].message.content}")
