import json
from services.db import insert_art_avg_weight

def load_cache_to_db():
    json_path = "cache.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for name, weight in data.items():
        insert_art_avg_weight(name, weight)

if __name__ == "__main__":
    load_cache_to_db()
