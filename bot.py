import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram import F
from dotenv import load_dotenv

from gpt_parser import extract_table_from_photo
from excel_builder import save_table_to_excel

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    photo_path = f"invoice.jpg"
    await bot.download_file(file.file_path, photo_path)

    table = extract_table_from_photo(photo_path)
    excel_path = save_table_to_excel(table, "invoice.xlsx")

    document = FSInputFile(excel_path)
    await message.answer_document(document, caption="✅ Ось Excel-файл")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
