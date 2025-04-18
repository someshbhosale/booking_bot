import requests
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# ------------------- STEP 1: Load Environment Variables -------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL"))  # Default: 10 minutes

API_URL = os.getenv("Ticket_Url")  # <-- Replace this with your actual API endpoint

# ------------------- STEP 2: Initialize In-Memory DB -------------------
known_event_codes = set()

# ------------------- STEP 3: Function to Send Telegram Notification -------------------
def send_telegram_message(match):
    message = (
        f"🏏 *New Match Alert!*\n"
        f"⚔ *{match['team_1']} vs {match['team_2']}*\n"
        f"🗓 {match['event_Display_Date']}\n"        
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.get(url, params=params)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# ------------------- STEP 4: Match Polling Loop -------------------
print("🔄 Starting API polling...")

while True:
    try:
        response = requests.get(API_URL,headers=headers, allow_redirects=True)
        data = response.json()
        matches = data.get("result", [])

        new_matches = []
        for match in matches:
            code = match["event_Code"]
            if code not in known_event_codes:
                known_event_codes.add(code)
                new_matches.append(match)

        for match in new_matches:
            send_telegram_message(match)
            print(f"✅ Sent alert for: {match['event_Name']}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] No new matches found." if not new_matches else f"[{timestamp}] {len(new_matches)} new matches found.")

    except Exception as e:
        print(f"❌ Error: {e}")

    time.sleep(CHECK_INTERVAL)
