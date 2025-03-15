from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from gtts import gTTS
import os

TOKEN = "8022352345:AAH6TBO_Y9LATeSnoaJkfA5L7zKHTLadrds"

async def start(update: Update, context):
    await update.message.reply_text("Kai-Khun Bot Ready! Hantar mesej dan aku akan balas dengan suara.")

async def handle_message(update: Update, context):
    text = update.message.text
    chat_id = update.message.chat.id

    # Convert teks ke suara guna gTTS
    tts = gTTS(text=text, lang="en")
    tts.save("voice.mp3")

    # Hantar voice ke Telegram
    with open("voice.mp3", "rb") as voice:
        await context.bot.send_voice(chat_id=chat_id, voice=voice)

    # Padam fail selepas dihantar
    os.remove("voice.mp3")

# Setup bot dengan `Application`
app = Application.builder().token(TOKEN).build()

# Tambah command dan message handler
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Jalankan bot
app.run_polling()

