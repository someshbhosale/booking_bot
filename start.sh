#!/bin/bash
apt-get update && apt-get install -y chromium
python3 test_bot.py  # Replace 'main.py' with your script filename
