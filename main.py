import requests
import json
import sys
import io
from data import search_knowledge

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = "http://localhost:8000/v1/chat/completions"

user_query = input("Введите ваш вопрос: ").strip()
knowledge_entries = search_knowledge(user_query)

context_block = "\n".join(
    f"- {entry['knowledge']}" for entry in knowledge_entries
)

json_prompt = f"""
Ниже представлен внутренний справочный материал компании:
{context_block}

На его основе ответьте на вопрос клиента:
{user_query}
"""

payload = {
    "model": "nous-hermes-2",
    "messages": [
        {"role": "system", "content": "Ты помощник логистической компании Pradius Nova, Республика Беларусь, Минский район, Папернянский сельсовет, 45/1 "
                                      "Ответ строго на русском языке. Соблюдай любезность и формализм в общении."},
        {"role": "user", "content": json_prompt.strip()}
    ],
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_tokens": 1000,
    "stream": True
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, stream=True)

if response.status_code == 200:
    try:
        response.encoding = 'utf-8'
        for line in response.iter_lines(decode_unicode=True):
            if line:
                if line.startswith("data: "):
                    line = line[len("data: "):]
                if line.strip() == "[DONE]":
                    break
                try:
                    json_data = json.loads(line)
                    delta = json_data["choices"][0]["delta"]
                    content = delta.get("content", "")
                    print(content, end='', flush=True)
                except json.JSONDecodeError:
                    print(f"[Ошибка разбора JSON]: {line}")
    except Exception as e:
        print(f"[Ошибка]: {e}")
else:
    print(f"Ошибка запроса: {response.status_code}")
