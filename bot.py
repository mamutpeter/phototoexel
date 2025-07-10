import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters
from gpt_parser import extract_table_from_photo
from excel_exporter import save_to_excel
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені фото рахунку, і я перетворю його у Excel-файл.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"temp/{photo.file_id}.jpg"
    await file.download_to_drive(file_path)

    try:
        table_data = extract_table_from_photo(file_path)
        excel_path = save_to_excel(table_data, photo.file_id)

        with open(excel_path, "rb") as f:
            await update.message.reply_document(f, filename="result.xlsx")

    except Exception as e:
        await update.message.reply_text(f"Помилка: {str(e)}")

# --------------- запуск одразу при імпорті ----------------

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
