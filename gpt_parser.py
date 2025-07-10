import os
import openai
import base64
import json
import re
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_table_from_photo(image_path: str):
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ти — парсер рахунків. Поверни ТІЛЬКИ JSON-масив (список обʼєктів), "
                    "без пояснень, без форматування, без ```json. Не додавай нічого окрім JSON."
                )
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

    raw_content = response.choices[0].message.content
    print("[GPT RESPONSE]")
    print(raw_content)
    print("----------------")

    try:
        return json.loads(raw_content)
    except json.JSONDecodeError:
        print("❗ JSON розпізнати не вдалося. Пробуємо fallback Markdown парсинг.")
        return markdown_fallback(raw_content)

def markdown_fallback(markdown_table: str) -> list:
    rows = [
        [cell.strip() for cell in re.split(r'\s*\|\s*', row.strip())[1:-1]]
        for row in markdown_table.strip().split('\n')
        if '|' in row and not re.match(r'^\s*\|[\s:-]+\|\s*$', row)
    ]
    if not rows or len(rows) < 2:
        raise ValueError("Не вдалося витягнути таблицю з markdown fallback.")
    header, *data = rows
    return [dict(zip(header, row)) for row in data]
