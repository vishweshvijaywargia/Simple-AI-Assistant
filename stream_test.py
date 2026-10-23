import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")            
)

full_response = ""
stream = client.chat.completions.create(
    model = os.getenv("MODEL"),
    messages = [
        {"role": "user", "content": "What is API? Give me answer in 100 words."}
    ],
    stream = True
)

for chunk in stream:
    piece = chunk.choices[0].delta.content
    if piece:
        full_response += piece
        print(piece, end="", flush=True)  
