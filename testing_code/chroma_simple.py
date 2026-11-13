import chromadb
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

embedding_model = os.getenv("EMBEDDING_MODEL")

chunks = {
    "c0" : "Leave Policy: Employees are entitled to 20 days of paid leave per year. Leave requests must be submitted at least 2 weeks in advance.",
    "c1" : "Hiring Process: The hiring process includes resume screening, initial interview, technical assessment, and final interview. Candidates will be notified of their status within 2 weeks.",
    "c2" : "Travel Policy: Employees must submit travel requests for approval at least 1 week in advance. Reimbursement will be provided for approved travel expenses.",
    "c3" : "Tech Docs: Project Deployment should Complete within a week. The deployment process includes code review, testing, and final approval from the project manager."
}

ids = list(chunks.keys())
documents = list(chunks.values())

embeddings = []
for doc in documents:
    response = client.embeddings.create(
        model=embedding_model,
        input=doc
    )
    embeddings.append(response.data[0].embedding)


dbclient = chromadb.PersistentClient(path = "./chroma_db")

vijayvargiya_associates = dbclient.get_or_create_collection(
   name = "vijayvargiya_associates",
   configuration = {
       "hnsw" : {
        "space" : "cosine",
       }
}
)

vijayvargiya_associates.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)

user_query = "What is the minimum time required for project deployment?"
user_embedding = client.embeddings.create(
    model=embedding_model,
    input=user_query
)

results = vijayvargiya_associates.query(
    query_embeddings=[user_embedding.data[0].embedding],
    n_results = 1 #top 1 result
)

print(results["documents"][0])