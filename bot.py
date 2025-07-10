import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from gpt_parser import extract_table_from_photo
from excel_builder import save_table_to_excel
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = await file.download_to_drive("invoice.jpg")

    table = extract_table_from_photo("invoice.jpg")
    excel_path = save_table_to_excel(table, "invoice.xlsx")

    await update.message.reply_document(document=InputFile(excel_path), filename="invoice.xlsx")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
