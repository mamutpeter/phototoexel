import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_table_from_photo(photo_path: str) -> list[list[str]]:
    with open(photo_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Витягни таблицю з цього фото у вигляді масиву масивів рядків."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        "max_tokens": 2000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    content = response.json()["choices"][0]["message"]["content"]

    return eval(content)  # ⚠️ Будь обережним — краще використовуй JSON, якщо GPT відповідає у форматі.
