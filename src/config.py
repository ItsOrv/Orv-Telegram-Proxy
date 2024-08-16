# config.py

import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
channel_id = int(os.getenv('CHANNEL_ID'))  # Ensure channel_id is an integer

proxy_channel_url = os.getenv('PROXY_CHANNEL_URL')
config_channel_url = os.getenv('CONFIG_CHANNEL_URL')
bot_url = os.getenv('BOT_URL')
support_url = os.getenv('SUPPORT_URL')
