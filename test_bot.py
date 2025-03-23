import time
import re
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from datetime import datetime

# ------------------- STEP 1: Initialize Variables -------------------
matches_db = []  # In-memory storage for match data
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
# CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL"))  # Check every 10 seconds
CHECK_INTERVAL = 900

# ------------------- STEP 2: Set Up Selenium -------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())

def fetch_matches():
    """Scrapes match data from the website and returns a list of matches."""
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://shop.royalchallengers.com/ticket/")
    time.sleep(5)  # Wait for page to load
    page_text = driver.find_element(By.TAG_NAME, "body").text
    driver.quit()

    # Regex Patterns
    match_pattern = re.compile(r"Royal Challengers Bengaluru\s+VS\s+([\w\s]+)")
    date_pattern = re.compile(r"\w{3}, \w{3} \d{2}, \d{4} \d{2}:\d{2} (AM|PM)")

    # Extract matches
    opponents = match_pattern.findall(page_text)
    match_dates = date_pattern.findall(page_text)

    # Ensure lists are aligned
    total_matches = min(len(opponents), len(match_dates))
    new_matches = []

    for i in range(total_matches):
        new_matches.append({
            "date": match_dates[i],
            "team1": "Royal Challengers Bengaluru",
            "team2": opponents[i].strip(),
        })
    
    return new_matches

def send_telegram_message(match):
    """Sends a match update to Telegram."""
    message = f"🏏 New Match Found!\n⚔ {match['team1']} vs {match['team2']}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(url, params=params)

# ------------------- STEP 3: Infinite Match Check Loop -------------------
print("🔄 Starting match checker...")

while True:
    matches = fetch_matches()

    for match in matches:
        if match not in matches_db:  # Only add if it's new
            matches_db.append(match)
            send_telegram_message(match)
            print(f"✅ New Match Added: {match['team1']} vs {match['team2']} on {match['date']}")
        
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] No New Match Found")
    time.sleep(CHECK_INTERVAL)  # Wait before checking again
