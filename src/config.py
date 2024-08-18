import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
channel_id = os.getenv('CHANNEL_ID') #orv_proxy

proxy_channel_url = os.getenv('PROXY_CHANNEL_URL') #https://t.me...
config_channel_url = os.getenv('CONFIG_CHANNEL_URL') #https://t.me...
bot_url = os.getenv('BOT_URL') #https://t.me...
support_url = os.getenv('SUPPORT_URL') #https://t.me...

channels = os.getenv('CHANNELS').split(',') #12342342 234124 12341234 1524213 12341234
