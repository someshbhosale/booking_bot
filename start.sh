# Update & Install Chromium for Railway
apt-get update && apt-get install -y chromium chromium-driver

# Set PATH for Chromium WebDriver
export CHROME_BIN=/usr/bin/chromium
export CHROMEDRIVER_PATH=/usr/bin/chromedriver
python3 test_bot.py  # Replace 'main.py' with your script filename
