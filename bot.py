import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

load_dotenv()  # Завантажує змінні середовища з .env

API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise RuntimeError("BOT_TOKEN not found in environment variables")

# Налаштування логування
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Я бот. Чим можу допомогти?")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
