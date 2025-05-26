import requests
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    url = "http://localhost:8001/v1/chat/completions"
    user_query = input("Enter the product title: ").strip()

    with open("categories.json", "r", encoding="utf-8") as f:
        weights = json.load(f)

    categories_list = list(weights.keys())
    categories_str = ", ".join(categories_list)

    prompt = f"""
You are an assistant that receives a product title and MUST assign it to EXACTLY ONE of these categories:
{categories_str}.

Output ONLY the category name exactly as above, nothing else.
Input product title:
{user_query}

Output category:
"""

    payload = {
        "messages": [
            {"role": "system", "content": "You assign product category from fixed list."},
            {"role": "user", "content": prompt.strip()}
        ],
        "temperature": 0.0,
        "max_tokens": 25,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        category = data["choices"][0]["message"]["content"].strip()
        print(f"Product category: {category}")

        weight = weights.get(category, 1000)
        print(f"Predicted weight (grams): {weight}")
    else:
        print(f"Request error: {response.status_code}")

if __name__ == "__main__":
    main()
