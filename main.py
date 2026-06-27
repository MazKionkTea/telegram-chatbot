import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Konfigurasi Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Konfigurasi API
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
LLAMA_SERVER_URL = "http://localhost:8080/v1/chat/completions"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirim pesan sambutan saat perintah /start dijalankan."""
    await update.message.reply_text("Halo! Saya adalah bot AI yang terhubung dengan llama.cpp. Silakan kirim pesan.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Memproses pesan masuk dan mendapatkan respons dari llama-server."""
    user_message = update.message.text

    # Payload untuk llama-server (format OpenAI compatible)
    payload = {
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    try:
        # Mengirim permintaan ke llama-server
        response = requests.post(LLAMA_SERVER_URL, json=payload, timeout=60)
        response.raise_for_status()

        # Mengambil teks respons
        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        logging.error(f"Error mendatangi llama-server: {e}")
        ai_reply = "Maaf, terjadi kesalahan saat menghubungi server AI."

    # Mengirim kembali respons ke pengguna Telegram
    await update.message.reply_text(ai_reply)

def main() -> None:
    """Menjalankan bot."""
    # Membangun aplikasi bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Menambahkan handler perintah dan pesan
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Memulai bot (polling mode)
    application.run_polling()

if __name__ == "__main__":
    main()
