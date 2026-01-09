import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Load env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise RuntimeError("❌ Missing TELEGRAM_BOT_TOKEN or GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

# Human-like system prompt
SYSTEM_PROMPT = """
You are chatting like a real human.
Be friendly, casual, and natural.
Use simple words.
Avoid robotic or formal tone.
Show empathy when needed.
Keep replies short and conversational.
Ask follow-up questions when appropriate.
Use Hinglish when the user uses Hinglish.
"""

# Memory (per user)
user_memory = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    history = user_memory.get(user_id, [])

    prompt_text = SYSTEM_PROMPT + "\n"
    for h in history:
        prompt_text += f"{h['role']}: {h['text']}\n"
    prompt_text += f"user: {text}\nassistant:"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GEMINI_API_KEY
    }

    try:
        r = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=30)
        data = r.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        reply = "Server thoda busy hai 😅 thodi der baad try karo."

    # Save memory (last 6 messages)
    history.append({"role": "user", "text": text})
    history.append({"role": "assistant", "text": reply})
    user_memory[user_id] = history[-6:]

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Gemini Telegram Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
