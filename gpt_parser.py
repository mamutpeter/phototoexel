import os
import openai
import base64
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_table_from_photo(image_path: str) -> list:
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Ти — парсер рахунків. Поверни лише таблицю у вигляді списку обʼєктів JSON (масив обʼєктів, без Markdown, без тексту)."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Ось фото рахунку. Витягни таблицю у форматі JSON:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=2000,
    )

    # Парсимо текст-відповідь як JSON
    return json.loads(response.choices[0].message.content)
