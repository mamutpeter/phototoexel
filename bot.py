import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv

from gpt_parser import extract_table_from_photo
from excel_builder import save_table_to_excel

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file_path = await photo.download(destination_file="invoice.jpg")

    table = extract_table_from_photo("invoice.jpg")
    excel_path = save_table_to_excel(table, "invoice.xlsx")

    await message.reply_document(FSInputFile("invoice.xlsx"), caption="Ось твій Excel ✅")


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
