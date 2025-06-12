from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

LLAMA_SERVER_URL = "http://localhost:8001/v1/chat/completions"
SYSTEM_PROMPT = (
    "You must respond with STRICTLY ONLY a JSON object containing a single field "
    "\"weight\" (an integer in GRAMS, always greater than zero). NO explanations, NO extra text, NO formatting. "
    "For example: {\"weight\": 1234}. "
    "Predict the weight based on the product name as the weight of one unit."
)

@app.route('/weight', methods=['POST'])
def predict_weight():
    prompt = request.form.get("product_name") or request.args.get("product_name")
    if not prompt:
        return jsonify({"error": "Missing 'product_name' field"}), 400

    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 25,
        "stream": False
    }

    try:
        response = requests.post(LLAMA_SERVER_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Error contacting llama server: {str(e)}"}), 500

    result_json = response.json()
    content = result_json["choices"][0]["message"]["content"].strip()

    try:
        weight_data = json.loads(content)
    except json.JSONDecodeError:
        weight_data = {"raw_response": content}

    return jsonify(weight_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
