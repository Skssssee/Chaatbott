import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY missing in .env")

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

SYSTEM_PROMPT = """
You are chatting like a real human.
Be friendly, casual, and natural.
Use simple words.
Avoid robotic or formal tone.
Show empathy when needed.
Keep replies short and conversational.
If the user uses Hinglish, reply in Hinglish.
Ask follow-up questions when it feels natural.
"""

def ask_gemini(user_message):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {"text": user_message}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY
    }

    r = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    if r.status_code != 200:
        return f"❌ Error: {r.text}"

    data = r.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ No response"

def main():
    print("🤖 Gemini AI Chat (type 'exit' to quit)")
    print("-" * 40)

    while True:
        user = input("👤 You: ").strip()

        if user.lower() in ["exit", "quit"]:
            print("👋 Bye! Take care.")
            break

        reply = ask_gemini(user)
        print(f"🤖 Gemini: {reply}\n")

if __name__ == "__main__":
    main()
