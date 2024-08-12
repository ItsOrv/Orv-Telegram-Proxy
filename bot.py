from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonUrl
from config import api_id, api_hash, bot_token, channels, channel_id
import re
import requests
import json
import os

# Initialize client and bot
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

PROXY_FILE = 'proxies.json'


def load_proxies():
    if not os.path.exists(PROXY_FILE):
        return {}
    with open(PROXY_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_proxies(proxies):
    with open(PROXY_FILE, 'w') as f:
        json.dump(proxies, f, indent=4)


def is_proxy_logged(link):
    proxies = load_proxies()
    for entry in proxies.values():
        if entry.get('link') == link:
            return True
    return False


def log_proxy(link, country, ip, port):
    proxies = load_proxies()
    proxy_id = str(len(proxies) + 1)
    proxies[proxy_id] = {
        'link': link,
        'Country': country,
        'IP': ip,
        'Port': port
    }
    save_proxies(proxies)


@client.on(events.NewMessage(chats=channels))
async def my_event_handler(event):
    message = event.message.message
    proxy_links = re.findall(r'https?://t\.me/proxy\?\S+', message)
    if not proxy_links:
        return
    for link in proxy_links:
        try:
            server = re.search(r'server=([^&]+)', link).group(1)
            port = re.search(r'port=([^&]+)', link).group(1)

            if is_proxy_logged(link):
                print(f"Proxy already logged: {link}")
                continue

            response = requests.get(f'http://ip-api.com/json/{server}')
            response.raise_for_status()
            country = response.json().get('country', 'Unknown')

            log_proxy(link, country, server, port)

            display_ip = server
            if len(display_ip) > 16:
                display_ip = display_ip[:16] + '.etc'

            text = f"**Orv\n\n• Country: {country} \n• IP: {display_ip} \n• Port: {port} \n\n**[proxy](https://t.me/Orv_Proxy)~[config](https://t.me/Orv_Vpn)~[bot](https://t.me/OrBSup_bot)~[support](https://t.me/OrvSup_bot)"
            buttons = [[KeyboardButtonUrl('Connect', link)]]
            await bot.send_message(channel_id, text, buttons=buttons, link_preview=False)
        except (AttributeError, requests.RequestException) as e:
            print(f"Error processing link {link}: {e}")


client.start()
client.run_until_disconnected()
