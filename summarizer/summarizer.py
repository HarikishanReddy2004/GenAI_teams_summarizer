import os
import requests
from config import gemini_api
# Set your API key here or via environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", gemini_api)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_summary(text, instruction="Summarize the following text clearly and concisely into two points  by removing unwanted discussion or random talk and remove headings like **Summary** ,**Updates** etc.."):
    if not text.strip():
        return "Input text is empty."

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [
                {"text": f"{instruction}\n\n{text}"}
            ]
        }],
        "generationConfig": {
            "temperature": 0.5,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 150
        }
    }

    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"
