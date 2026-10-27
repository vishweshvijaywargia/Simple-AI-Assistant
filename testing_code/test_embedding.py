from openai import OpenAI
from dotenv import load_dotenv 
import os 
load_dotenv() #by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

response  = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"), 
    input = ["He is a good boy", "Python is a programming language"]
)

for i, embedding in enumerate(response.data):
    print(f"Embedding for input {i}: {embedding.embedding[:5]}...")  # Print first 5 dimensions for brevity

print(len(response.data[0].embedding))  # Print the length of the embedding vector