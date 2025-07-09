import openai
import os
from dotenv import load_dotenv
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def extract_table_from_photo(image_path: str):
    base64_image = encode_image_to_base64(image_path)

    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Розпізнай таблицю з накладної на фото та поверни її як масив рядків, кожен з яких — це список значень колонок. Не пиши жодних пояснень, тільки масив у форматі JSON."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=2000
    )

    import json
    try:
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print("Parsing error:", e)
        return [["Не вдалося розпізнати таблицю"]]
