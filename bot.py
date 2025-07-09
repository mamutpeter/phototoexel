import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from gpt_parser import extract_table_from_photo
from excel_builder import save_table_to_excel
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    file_path = await photo_file.download_to_drive("invoice.jpg")

    table = extract_table_from_photo("invoice.jpg")
    excel_path = save_table_to_excel(table, "invoice.xlsx")

    await update.message.reply_document(document=InputFile(excel_path), filename="invoice.xlsx")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
