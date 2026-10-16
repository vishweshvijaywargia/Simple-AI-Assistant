
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv() # Load environment variables from .env file
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP

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
while True:
    user_input = input("\n You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools = TOOLS
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments or "{}") #convert string to dict, if no arguments, use empty dict
            func = FUNCTION_NAME_TO_FUNCTION_MAP.get(function_name)

            result = func(**function_args) if func else None #dictionary unpacking
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        res = client.chat.completions.create( #2nd time call so that we can get the final response from the assistant after tool execution
            model=os.getenv("MODEL"),
            messages=messages
        )

        msg = res.choices[0].message

    messages.append({"role": "assistant", "content": msg.content})

    print(f"\n Assistant: {msg.content}")
