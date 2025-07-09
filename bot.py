import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from gpt_parser import extract_table_from_photo
from excel_builder import save_table_to_excel

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("👋 Надішли фото рахунку-фактури, і я зроблю з нього Excel-файл.")


@dp.message(types.ContentType.PHOTO)
async def photo_handler(message: types.Message):
    photo = message.photo[-1]
    await photo.download(destination_file="invoice.jpg")

    table = extract_table_from_photo("invoice.jpg")
    path = save_table_to_excel(table, "invoice.xlsx")

    await message.reply_document(FSInputFile(path), caption="Ось твій Excel ✅")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
