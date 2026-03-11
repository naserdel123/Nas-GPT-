from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# قراءة API Key من متغير البيئة
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# دالة الدردشة (GPT)
def ask_ai(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": message}]
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]

# دالة إنشاء الصور (DALL·E)
def generate_image(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "512x512"
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result["data"][0]["url"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data["message"]
    reply = ask_ai(message)
    return jsonify({"reply": reply})

@app.route("/image", methods=["POST"])
def image():
    data = request.json
    prompt = data["prompt"]
    image_url = generate_image(prompt)
    return jsonify({"image": image_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
