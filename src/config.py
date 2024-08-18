# config.py
# loads runtime settings from the .env file

import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
channel_id = os.getenv('CHANNEL_ID')

proxy_channel_url = os.getenv('PROXY_CHANNEL_URL')
config_channel_url = os.getenv('CONFIG_CHANNEL_URL')
bot_url = os.getenv('BOT_URL')
support_url = os.getenv('SUPPORT_URL')

# Load channels as a list of integers
_raw_channels = os.getenv('CHANNELS', '')
channels = [int(c.strip()) for c in _raw_channels.split(',') if c.strip()]

# Warn early if no channels were provided
if not channels:
    print("Warning: CHANNELS is empty, the bot will not monitor anything")
