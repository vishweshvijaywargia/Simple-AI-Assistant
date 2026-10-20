from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv() # Load environment variables from .env file
from tools import TOOLS, run_tool
from utilities.utilities import log

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
)

messages = []

messages.append(
    {
        "role": "system",
        "content": "You are a helpful assistant"
    }
)

MAX_STEPS = 5

while True:
    user_input = input("\n You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    messages.append({"role": "user", "content": user_input})

    #Chained Tool Calling
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools = TOOLS
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        log(f"Step - {step + 1}: Model requested {len(msg.tool_calls)} tool call(s): {[tool_call.function.name for tool_call in msg.tool_calls]}")

        messages.append(msg)

        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

    else:
        print("Maximum steps reached. The assistant could not provide a final answer.")
        messages.append({"role": "assistant", "content": "Maximum steps reached. The assistant could not provide a final answer."})
        continue

    messages.append({"role": "assistant", "content": msg.content})

    print(f"\n Assistant: {msg.content}")
