
import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8142835960:AAGyhJitBvVKIMbgtWj1XTRhC3ByDEtMIdU"

DOWNLOAD_PATH = "./downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Torrent bot ishga tushdi! Magnet link yoki .torrent fayl yuboring.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("magnet:?"):
        await update.message.reply_text("Yuklash boshlandi...")
        subprocess.run(["aria2c", "--dir=" + DOWNLOAD_PATH, text])
        await update.message.reply_text("Yuklash tugadi!")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    file_path = os.path.join(DOWNLOAD_PATH, doc.file_name)
    new_file = await doc.get_file()
    await new_file.download_to_drive(file_path)

    await update.message.reply_text("Torrent fayl yuklandi, yuklash boshlanmoqda...")
    subprocess.run(["aria2c", "--dir=" + DOWNLOAD_PATH, file_path])
    await update.message.reply_text("Yuklash tugadi!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    print("Bot ishga tushdi!")
    app.run_polling()
