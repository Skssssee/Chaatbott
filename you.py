import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔐 NEVER hardcode real keys in public repos
TELEGRAM_BOT_TOKEN = "8401058181:AAG3VeCcixxdX9K91RAyGMmWpHi9uy55IP8"
XAI_API_KEY = "xai-7p2PAwAq5hwRXJ4UUFk4Qm6soECFfPXpn1WrxXYGLkBR4DiAZ7A4ADU9QiSTVXuWYbMiXwrlx0hkNcrf"

XAI_URL = "https://api.x.ai/v1/chat/completions"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2",
        "messages": [
            {"role": "system", "content": "You are a helpful Telegram chatbot."},
            {"role": "user", "content": user_msg}
        ]
    }

    try:
        res = requests.post(XAI_URL, headers=headers, json=payload, timeout=30)
        data = res.json()

        reply = data["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("❌ Error from Grok API")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
