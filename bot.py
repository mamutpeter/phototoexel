import os
from telegram import Update, InputFile
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv
from gpt_parser import extract_table_from_photo
from excel_builder import save_table_to_excel

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Надішли фото рахунку – я згенерую Excel-файл з таблицею."
    )

# Фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive("invoice.jpg")

    table_data = extract_table_from_photo("invoice.jpg")
    excel_path = save_table_to_excel(table_data, "invoice.xlsx")

    # Важливо: відкриваємо файл вручну і явно задаємо filename
    with open("invoice.xlsx", "rb") as file:
        await update.message.reply_document(
            document=InputFile(file, filename="invoice.xlsx")
        )

# Головна функція
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
