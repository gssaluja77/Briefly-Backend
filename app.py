from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS
from config import system_message, concise, detailed, bullets

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL")
OPENROUTER_API_MODEL = os.getenv("OPENROUTER_API_MODEL")

system_prompt = {
    "system_message": system_message,
    "concise": concise,
    "detailed": detailed,
    "bullets": bullets,
}

@app.route("/api/briefly", methods=["POST"])
def summarizer():
    try:
        data = request.get_json()
        summary_type = data.get("type", "concise")
        text_to_summarize = data.get("content", "")
        system_msg = system_prompt.get("system_message") + system_prompt.get(summary_type, system_prompt["concise"])

        payload = {
            "model": OPENROUTER_API_MODEL,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text_to_summarize},
            ],
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500