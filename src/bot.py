# bot.py

from telethon import TelegramClient, events, Button
from config import api_id, api_hash, bot_token, channels, proxy_channel_url, config_channel_url, bot_url, support_url, channel_id
import requests
import re
import logging
import os
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO)

# File to store proxies
PROXY_FILE = 'proxies.txt'

# Initialize client and bot
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def clean_old_proxies():
    """Remove the proxy file if it exists."""
    if os.path.exists(PROXY_FILE):
        os.remove(PROXY_FILE)

async def schedule_cleaning():
    """Schedule the cleaning task every 24 hours."""
    while True:
        await clean_old_proxies()
        await asyncio.sleep(86400)  # Sleep for 24 hours

def is_proxy_logged(proxy):
    """Check if the proxy has been logged in the proxy file."""
    if not os.path.exists(PROXY_FILE):
        return False

    with open(PROXY_FILE, 'r') as file:
        for line in file:
            logged_proxy = line.strip()
            if proxy == logged_proxy:
                return True
    return False

def log_proxy(proxy):
    """Log the proxy to the file."""
    with open(PROXY_FILE, 'a') as file:
        file.write(f"{proxy}\n")

@client.on(events.NewMessage(chats=channels))
async def my_event_handler(event):
    message = event.message.message
    proxy_links = re.findall(r'https?://t\.me/proxy\?\S+', message)
    if proxy_links:
        for link in proxy_links:
            try:
                server = re.search(r'server=([^&]+)', link).group(1)
                port = re.search(r'port=([^&]+)', link).group(1)
                proxy = f"{server}:{port}"
                
                if is_proxy_logged(proxy):
                    logging.info(f"Proxy {proxy} has been used in the last 24 hours.")
                    continue

                response = requests.get(f'http://ip-api.com/json/{server}')
                response.raise_for_status()
                location = response.json().get('country', 'Unknown')

                if len(server) > 16:
                    server = server[:16] + '.etc'

                text = (
                    f"**〰️Orv〰️\n\n"
                    f"• Country: {location} \n"
                    f"• IP: {server} \n"
                    f"• Port: {port} \n\n"
                    f"**[proxy]({proxy_channel_url})~[config]({config_channel_url})~[bot]({bot_url})~[support]({support_url})"
                )
                buttons = [Button.url('Connect', link)]
                await bot.send_message(channel_id, text, buttons=buttons, link_preview=False)

                # Log the proxy
                log_proxy(proxy)

            except AttributeError:
                logging.error(f"Error parsing link: {link}. Required parameters missing.")
            except requests.RequestException as e:
                logging.error(f"Error fetching data for {server}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")

async def main():
    # Ensure full connection
    await client.start()

    # Schedule the cleaning task
    asyncio.create_task(schedule_cleaning())

    # Run the bot
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
