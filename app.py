from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"

def ask_ai(message):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    return result["choices"][0]["message"]["content"]

@app.route("/")
def home():
    return "AI Server Running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]

    reply = ask_ai(message)

    return jsonify({"reply": reply})

app.run(host="0.0.0.0", port=10000)
