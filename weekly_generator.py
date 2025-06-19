import os
import requests
from datetime import datetime, timedelta
from config import gemini_api
# Set your API key here or via environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", gemini_api)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def collect_weekly_text(folder_path):
    weekly_text = ""
    # today = datetime.today()

    # Scan all .txt files in the folder from the past 7 days
    for file_name in os.listdir(folder_path):
        if not file_name.endswith(".txt"):
            continue

        with open(os.path.join(folder_path, file_name), "r") as file:
            weekly_text += file.read().strip() + "\n"
 

    return weekly_text.strip()

def summarize_weekly_text(text):
    if not text:
        return "No summaries found for the week."

    headers = {"Content-Type": "application/json"}
    instruction = (
        "Summarize the following weekly team updates max into 3 crisp bullet points. And also mention what Isses faced under issue heading"
        "Do not include personal names, PRs, or story IDs. Focus only on key accomplishments,completed tasks, integrations, or validations. "
        "frame summary points which should be very generic it should be like--> I finished this or that.It should basically give the headings which we focused whole week ."
        "Ensure this update report will be monitored by the leadership team .so make sure it shouldn't contain non-work related and also basic works.It shoudl cover all week files into few points "
        "No * marks present, and also there shouldn't be the natural language statements such as here is the updated summary/ whaterver u try to explain."
    )

    payload = {
        "contents": [{
            "parts": [{"text": f"{instruction}\n\n{text}"}]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 700
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

def generate_weekly_report(folder_path):
    print(f"Collecting summaries from: {folder_path}")
    raw_text = collect_weekly_text(folder_path)
    if not raw_text:
        print("No data collected.")
        return

    print("Generating weekly summary...\n")
    summary = summarize_weekly_text(raw_text)
    print(summary)
    report_dir = "D:\\teams_genai\\venv\\weekly_report"
    weekly_file = os.path.join(report_dir, 'current_week_report.txt')
    with open(weekly_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"All summaries written to {weekly_file}")
