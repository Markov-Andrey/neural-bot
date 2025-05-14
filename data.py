import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def search_knowledge(query: str, vector_file="vector.json", data_file="data.json", top_k=5):
    query_vector = model.encode(query)
    with open(vector_file, "r", encoding="utf-8") as f:
        vector_data = json.load(f)["data"]
    ids = [item["id"] for item in vector_data]
    vectors = np.array([item["vector"] for item in vector_data])
    similarities = cosine_similarity([query_vector], vectors)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    top_ids = [ids[i] for i in top_indices]
    with open(data_file, "r", encoding="utf-8") as f:
        full_data = json.load(f)["data"]
    relevant_knowledge = []
    for entry in full_data:
        if entry["id"] in top_ids:
            relevant_knowledge.append({
                "id": entry["id"],
                "context": entry["context"],
                "knowledge": entry["knowledge"]
            })
    return relevant_knowledge
