import os
import re
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonUrl

# Load environment variables from .env file
load_dotenv()

# Values from .env file
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SESSION_NAME = os.getenv('SESSION_NAME', 'session_name')

# Initialize client and bot
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Channels to monitor
MONITORED_CHANNELS = [1872519774, 1535855645, 6663338157]

@client.on(events.NewMessage(chats=MONITORED_CHANNELS))
async def handle_new_message(event):
    message = event.message.message
    proxy_links = re.findall(r'https?://t\.me/proxy\?\S+', message)
    
    if proxy_links:
        for link in proxy_links:
            try:
                server = re.search(r'server=([^&]+)', link).group(1)
                port = re.search(r'port=([^&]+)', link).group(1)
                response = requests.get(f'http://ip-api.com/json/{server}')
                response.raise_for_status()

                location = response.json().get('country', 'Unknown')
                if len(server) > 16:
                    server = server[:16] + '...'
                
                text = (f"**〰️Orv〰️\n\n"
                        f"• Country: {location}\n"
                        f"• IP: {server}\n"
                        f"• Port: {port}\n\n"
                        f"**[proxy](https://t.me/Orv_Proxy)~"
                        f"[config](https://t.me/Orv_Vpn)~"
                        f"[bot](https://t.me/OrBSup_bot)~"
                        f"[support](https://t.me/OrvSup_bot)")
                
                buttons = [[KeyboardButtonUrl('Connect', link)]]
                await bot.send_message('orv_proxy', text, buttons=buttons, link_preview=False)
            
            except (AttributeError, requests.RequestException) as e:
                print(f"Error processing link {link}: {e}")

client.start()
client.run_until_disconnected()
