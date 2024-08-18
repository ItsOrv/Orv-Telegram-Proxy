from telethon import TelegramClient, events, Button
from telethon.tl.types import KeyboardButtonUrl
from config import api_id, api_hash, bot_token, channel_id, proxy_channel_url, config_channel_url, bot_url, support_url, channels
import requests
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize client and bot
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Resolve channel entities
resolved_channels = []
for chat in channels:
    try:
        entity = client.loop.run_until_complete(client.get_input_entity(chat))
        resolved_channels.append(entity)
    except Exception as e:
        logging.error(f"Error resolving chat '{chat}': {e}")

@client.on(events.NewMessage(chats=resolved_channels))
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
                location = response.json().get('country', 'Unknown')

                # Truncate server address if necessary
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
            except AttributeError:
                logging.error(f"Error parsing link: {link}. Required parameters missing.")
            except requests.RequestException as e:
                logging.error(f"Error fetching data for {server}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")

client.start()
client.run_until_disconnected()
