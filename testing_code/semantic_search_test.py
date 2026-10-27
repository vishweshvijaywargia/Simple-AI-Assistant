from openai import OpenAI
from dotenv import load_dotenv 
import os 
import numpy as np
load_dotenv() #by default looks for .env file

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def get_embeddings(input_text):
    response  = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"), 
        input = input_text
    )
    return response.data[0].embedding


def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    return dot_product / (norm_A * norm_B)

embedding1 = get_embeddings("Python is a programming language")
embedding2 = get_embeddings("Python provides many libraries for data science")
embedding3 = get_embeddings("The weather is sunny today")

similarity1 = cosine_similarity(embedding1, embedding2)
similarity2 = cosine_similarity(embedding1, embedding3)

print(f"Similarity between embedding1 and embedding2: {similarity1:.4f}")
print(f"Similarity between embedding1 and embedding3: {similarity2:.4f}")