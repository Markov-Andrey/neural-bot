import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vector_data = []

for item in data["data"]:
    context_text = item["context"]
    vector = model.encode(context_text).tolist()
    vector_data.append({
        "id": item["id"],
        "vector": vector
    })

with open("vector.json", "w", encoding="utf-8") as f:
    json.dump({"data": vector_data}, f, indent=4, ensure_ascii=False)