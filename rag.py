import os
import numpy
import json
from openai import OpenAI
from dotenv import load_dotenv
from utilities.utilities import log

load_dotenv(override = True) #by default looks for .env file


client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
KB_FOLDER = os.getenv("KB_FOLDER")
VECTOR_STORE_JSON = os.getenv("VECTOR_STORE_JSON")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


#Get the embedding of a text from Embedding model
def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

#Get the cosine similarity between two vectors
def cosine_similarity(A, B):
    dot_prod = numpy.dot(A, B)
    norm_a = numpy.linalg.norm(A)
    norm_b = numpy.linalg.norm(B)
    return dot_prod / (norm_a * norm_b)

#Load the documents
def load_documents(folder=KB_FOLDER):
    documents = []

    if not folder:
        raise ValueError("KB_FOLDER is missing from the .env file")
    
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            documents.append(
                {
                    "source": filename,
                    "text":f.read(),
                }
            )
        
    return documents

#load chunks from the stored json file
def read_chunks():
    with open(VECTOR_STORE_JSON, "r", encoding = "utf8") as f:
        chunks = json.load(f)
    log(f"Readed the {len(chunks)} already saved chunks in the json file")
    return chunks

#write the chunks in the json file for the first time it is loaded
def write_chunks(chunks):
    with open(VECTOR_STORE_JSON, "w", encoding = "utf8") as f:
        json.dump(chunks, f, indent = 4)
    print("Save the chunks in json file for the first time")

#have appended chunks from each document
def create_chunks():
    chunks = []
    documents = load_documents()

    for document in documents:
        chunks.extend(chunk_document(document))
    return chunks

#create chunks for each document
def chunk_document(document):
    chunks = []
    chunk_id = 0
    for part in document["text"].split("\n\n"):
        part = part.strip()
        if part:
            chunks.append({
                "source": document["source"],
                "text" : part,
                "chunk_id" : chunk_id
            })
        chunk_id += 1
    
    return chunks

#Add embeddings in the chunks
def add_embeddings(chunks):
    for chunk in chunks:
        vector = get_embedding(chunk["text"])
        chunk["vector"] = vector
    
    return chunks

chunks = []
if(os.path.exists(VECTOR_STORE_JSON) and os.path.getsize(VECTOR_STORE_JSON) > 0):
    chunks = read_chunks()
else :
    chunks = create_chunks()
    chunks = add_embeddings(chunks)
    write_chunks(chunks)

#Search method to search the top_k chunks for a user_query
def search(query, top_k=3):
    query_vector = get_embedding(query)

    results = []
    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["vector"])
        results.append(
            {
                "score" : float(score),
                "source": chunk["source"],
                "text": chunk["text"],
                "chunk_id": chunk["chunk_id"],
                "size": len(chunk["text"])
            }
        )

    results.sort(key=lambda rec: rec["score"], reverse=True)
    return results[:top_k]
