from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from gtts import gTTS
from tempfile import NamedTemporaryFile
import os

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

async def start(update: Update, context):
    await update.message.reply_text("Kai-Khun Bot Ready! Hantar mesej dan aku akan balas dengan suara.")

async def handle_message(update: Update, context):
    text = update.message.text
    chat_id = update.message.chat.id

    # Convert teks ke suara guna gTTS
    tts = gTTS(text=text, lang="en")
    # Simpan hasil tts dalam fail sementara
    with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.write_to_fp(tmp_file)
        tmp_file.flush()
        tmp_file.seek(0)
        await context.bot.send_voice(chat_id=chat_id, voice=tmp_file)

    # Padam fail selepas dihantar
    os.remove(tmp_file.name)

# Setup bot dengan `Application`
app = Application.builder().token(TOKEN).build()

# Tambah command dan message handler
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Jalankan bot
app.run_polling()

