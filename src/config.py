# config.py

import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
#str
channel_id = os.getenv('CHANNEL_ID')

proxy_channel_url = os.getenv('PROXY_CHANNEL_URL')
config_channel_url = os.getenv('CONFIG_CHANNEL_URL')
bot_url = os.getenv('BOT_URL')
support_url = os.getenv('SUPPORT_URL')

# Load channels as a list of integers
channels = [int(chat_id.strip()) for chat_id in os.getenv('CHANNELS').split(',')]
