import os
from dotenv import load_dotenv

# 🔴 FORCE load .env from same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ===== ENV VARS =====
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not XAI_API_KEY:
    raise RuntimeError("Env vars missing: TELEGRAM_BOT_TOKEN or XAI_API_KEY")

# ===== XAI CONFIG =====
XAI_URL = "https://api.x.ai/v1/chat/completions"
XAI_MODEL = "grok-2-latest"

# ===== HANDLER =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": XAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful Telegram chatbot."},
            {"role": "user", "content": user_msg}
        ]
    }

    try:
        r = requests.post(XAI_URL, headers=headers, json=payload, timeout=30)
        data = r.json()

        if "choices" not in data:
            await update.message.reply_text(str(data))
            return

        reply = data["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
