import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from openai import OpenAI
from dotenv import load_dotenv
from gpt_parser import extract_table_from_photo
from excel_builder import save_table_to_excel

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file_path = f"invoice_{message.from_user.id}.jpg"
    await photo.download(destination_file=file_path)

    # Обробка GPT і збереження Excel
    table = extract_table_from_photo(file_path)
    excel_path = save_table_to_excel(table, f"invoice_{message.from_user.id}.xlsx")

    await message.answer_document(InputFile(excel_path), caption="Ось ваш Excel-файл")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
