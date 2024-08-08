from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonUrl
import re
import requests

# values
api_id = ''
api_hash = ''
bot_token = ''

# Initialize client and bot
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=[]))
async def my_event_handler(event):
    message = event.message.message
    proxy_links = re.findall(r'https?://t\.me/proxy\?\S+', message)
    if proxy_links:
        for link in proxy_links:
            try:
                server = re.search(r'server=([^&]+)', link).group(1)
                port = re.search(r'port=([^&]+)', link).group(1)
                response = requests.get(f'http://ip-api.com/json/{server}')
                response.raise_for_status()
                location = response.json().get('country', 'idk')
                if len(server) > 16:
                    server = server[:16] + '.etc'
                text = f"**〰️Orv〰️\n\n• Country: {location} \n• IP: {server} \n• Port: {port} \n\n**[proxy](https://t.me/Orv_Proxy)~[config](https://t.me/Orv_Vpn)~[bot](https://t.me/OrBSup_bot)~[support](https://t.me/OrvSup_bot)"
                buttons = [[KeyboardButtonUrl('Connect', link)]]
                await bot.send_message('orv_proxy', text, buttons=buttons, link_preview=False)
            except (AttributeError, requests.RequestException) as e:
                print(f"Error processing link {link}: {e}")

client.start()
client.run_until_disconnected()
