import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
XAI_API_KEY = "NEW_XAI_API_KEY"   # 🔴 NEW KEY ONLY

XAI_URL = "https://api.x.ai/v1/chat/completions"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-latest",
        "messages": [
            {"role": "user", "content": user_msg}
        ]
    }

    try:
        r = requests.post(XAI_URL, headers=headers, json=payload, timeout=30)
        data = r.json()

        # 👇 DEBUG (IMPORTANT)
        if "choices" not in data:
            await update.message.reply_text(f"❌ Grok API Error:\n{data}")
            return

        reply = data["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"❌ Exception: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
