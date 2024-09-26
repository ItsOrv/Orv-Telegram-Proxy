from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonUrl
from config import api_id, api_hash, bot_token, channels, channel_id
import re
import requests
import json
import os
import socket
import time
import asyncio

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


def log_proxy(link, country, ip, port, ping=None):
    proxies = load_proxies()
    proxy_id = str(len(proxies) + 1)
    proxies[proxy_id] = {
        'link': link,
        'Country': country,
        'IP': ip,
        'Port': port
    }
    if ping is not None:
        proxies[proxy_id]['Ping'] = f"{ping}ms"
    save_proxies(proxies)


def ping_proxy(host, port, timeout=3):
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        if result == 0:
            return round((time.time() - start) * 1000, 2)
        return None
    except Exception as e:
        print(f"ping failed for {host}:{port}: {e}")
        return None


def get_country(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        response.raise_for_status()
        return response.json().get('country', 'Unknown')
    except requests.RequestException as e:
        print(f"Error getting country for {ip}: {e}")
        return 'Unknown'


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

            country = get_country(server)
            ping = ping_proxy(server, port)

            log_proxy(link, country, server, port, ping)

            display_ip = server
            if len(display_ip) > 16:
                display_ip = display_ip[:16] + '.etc'

            text = f"**Orv\n\n• Country: {country}\n• IP: {display_ip}\n• Port: {port}\n"
            if ping is not None:
                text += f"• Ping: {ping}ms\n"
            text += "\n**[proxy](https://t.me/Orv_Proxy)~[config](https://t.me/Orv_Vpn)~[bot](https://t.me/OrBSup_bot)~[support](https://t.me/OrvSup_bot)"

            buttons = [[KeyboardButtonUrl('Connect', link)]]
            await bot.send_message(channel_id, text, buttons=buttons, link_preview=False)
        except (AttributeError, requests.RequestException) as e:
            print(f"Error processing link {link}: {e}")


async def clean_old_proxies():
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'w') as f:
            json.dump({}, f, indent=4)
        print("cleaned old proxies file")


async def schedule_cleaning():
    while True:
        await asyncio.sleep(86400)  # once a day
        await clean_old_proxies()


client.start()
client.loop.create_task(schedule_cleaning())
client.run_until_disconnected()
