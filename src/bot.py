from telethon import TelegramClient, events, Button
from config import api_id, api_hash, bot_token, channels, proxy_channel_url, config_channel_url, bot_url, support_url, channel_id
import requests
import re
import logging
import os
import asyncio
import json

# Setup logging
logging.basicConfig(level=logging.INFO)

# File to store proxies
PROXY_FILE = 'proxies.json'

# Initialize client and bot
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def clean_old_proxies():
    """Remove the proxy file if it exists."""
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'w') as file:
            json.dump({}, file)

async def schedule_cleaning():
    """Schedule the cleaning task every 24 hours."""
    while True:
        await clean_old_proxies()
        await asyncio.sleep(86400)  # Sleep for 24 hours

def load_proxies():
    """Load proxies from the JSON file."""
    if not os.path.exists(PROXY_FILE):
        return {}

    with open(PROXY_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

def save_proxies(proxies):
    """Save proxies to the JSON file."""
    with open(PROXY_FILE, 'w') as file:
        json.dump(proxies, file, indent=4)

def is_proxy_logged(proxy):
    """Check if the proxy has been logged in the proxy file."""
    proxies = load_proxies()
    return any(entry['link'] == proxy for entry in proxies.values())

def log_proxy(proxy, country, ip, port):
    """Log the proxy to the JSON file."""
    proxies = load_proxies()
    proxy_id = str(len(proxies) + 1)
    proxies[proxy_id] = {
        'link': proxy,
        'Country': country,
        'IP': ip,
        'Port': port
    }
    save_proxies(proxies)

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

                if is_proxy_logged(link):
                    logging.info(f"Proxy {link} has been used in the last 24 hours.")
                    continue

                response = requests.get(f'http://ip-api.com/json/{server}')
                response.raise_for_status()
                location = response.json().get('country', 'Unknown')

                if len(server) > 16:
                    server = server[:16] + '.etc'

                text = (
                    f"**\u2774Orv\u2774\n\n"
                    f"\u2022 Country: {location} \n"
                    f"\u2022 IP: {server} \n"
                    f"\u2022 Port: {port} \n\n"
                    f"**[proxy]({proxy_channel_url})~[config]({config_channel_url})~[bot]({bot_url})~[support]({support_url})"
                )
                buttons = [Button.url('Connect', link)]
                await bot.send_message(channel_id, text, buttons=buttons, link_preview=False)

                # Log the proxy
                log_proxy(link, location, server, port)

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
