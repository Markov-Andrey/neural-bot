import requests
import json
import sys
import io
import oracledb
import difflib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def connect_to_oracle():
    oracledb.init_oracle_client()

    user = "bz_o"
    password = "ping"
    host = "192.168.241.10"
    port = 1521
    sid = "test"

    dsn = oracledb.makedsn(host, port, sid=sid)
    try:
        conn = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        print("✅ Подключение успешно!")
        conn.close()
    except oracledb.DatabaseError as e:
        print("❌ Ошибка подключения:", e)


def main():
    url = "http://localhost:8001/v1/chat/completions"
    user_query = input("Введите название товара: ").strip()

    try:
        oracledb.init_oracle_client()

        user = "bz_o"
        password = "ping"
        host = "192.168.241.10"
        port = 1521
        sid = "test"

        dsn = oracledb.makedsn(host, port, sid=sid)
        conn = oracledb.connect(user=user, password=password, dsn=dsn)

        cursor = conn.cursor()

        query_fuzzy = """
            SELECT ID, NAME, NET_WEIGHT FROM (
                SELECT ID, NAME, NET_WEIGHT,
                       UTL_MATCH.EDIT_DISTANCE(LOWER(NAME), LOWER(:query)) AS DIST
                FROM ART
                WHERE UTL_MATCH.EDIT_DISTANCE(LOWER(NAME), LOWER(:query)) <= 10
                ORDER BY DIST
            )
            WHERE ROWNUM <= 5
        """

        cursor.execute(query_fuzzy, {'query': user_query})
        rows = cursor.fetchall()

        if rows:
            print("🔍 Похожие товары:")
            for idx, (id, name, weight) in enumerate(rows):
                match = difflib.get_close_matches(user_query.lower(), [name.lower()], n=1, cutoff=0.1)
                matched_part = f" (совпадение: '{match[0]}')" if match else ""
                prefix = "🎯 Наиболее релевантный:" if idx == 0 else "-"
                print(f"{prefix} {id}: {name} - {weight} г{matched_part}")
        else:
            print("❌ Совпадений не найдено.")

        cursor.close()
        conn.close()

    except oracledb.DatabaseError as e:
        print("❌ Ошибка при работе с БД:", e)

    return
    json_prompt = f"""
    <|im_start|>system
    You are a model that MUST predict the weight in grams (integer) of a product based ONLY on its name.
    Ignore article numbers, model numbers, or SKU codes (e.g., 1.291-226.0) — they are NOT related to weight.
    Respond with EXACTLY one JSON object and NOTHING ELSE.

    Your output must include:
    - "weight": integer from 0 to 100000
    - "reason": a short explanation (1-2 sentences) of why this weight was assigned, based on the product name (excluding article numbers).

    Do NOT add explanations, comments, or any other text outside of the JSON object.
    <|im_end|>
    <|im_start|>user
    Input:
    {{
      "{user_query}"
    }}

    Output format:
    {{
      "weight": <integer weight in grams>,
      "reason": "<short explanation based on the product name>"
    }}
    <|im_end|>
    <|im_start|>assistant
    """

    payload = {
        "messages": [
            {"role": "system", "content": "You are a precise assistant that only outputs JSON objects with weight predictions."},
            {"role": "user", "content": json_prompt.strip()}
        ],
        "temperature": 0.2,
        "top_p": 0.7,
        "top_k": 10,
        "max_tokens": 500,
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
            print()
        except Exception as e:
            print(f"[Ошибка]: {e}")
    else:
        print(f"Ошибка запроса: {response.status_code}")


if __name__ == "__main__":
    connect_to_oracle()
    main()
