#bot.py
import json
from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonUrl, InlineKeyboardButton, InlineKeyboardMarkup
import re
import requests
from config import api_id, api_hash, bot_token, admin_id, db_path
from utils import save_data, load_data, refresh_groups

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Store user responses temporarily
user_responses = {}

async def start_handler(event):
    buttons = [
        [InlineKeyboardButton("Add Channel", callback_data='add_channel')],
        [InlineKeyboardButton("Remove Channel", callback_data='remove_channel')],
        [InlineKeyboardButton("Refresh Channels", callback_data='refresh_channels')],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(event.chat_id, 'Channel Management', buttons=reply_markup)

@bot.on(events.NewMessage(pattern="/start"))
async def start_command(event):
    await start_handler(event)

@bot.on(events.CallbackQuery(data=re.compile(b'add_channel')))
async def add_channel_handler(event):
    await bot.send_message(event.chat_id, 'Please send the channel ID:')
    user_responses[event.chat_id] = {'action': 'add_channel'}

@bot.on(events.CallbackQuery(data=re.compile(b'remove_channel')))
async def remove_channel_handler(event):
    await bot.send_message(event.chat_id, 'Please send the channel ID:')
    user_responses[event.chat_id] = {'action': 'remove_channel'}

@bot.on(events.CallbackQuery(data=re.compile(b'refresh_channels')))
async def refresh_channels_handler(event):
    await refresh_groups(bot)
    await bot.send_message(event.chat_id, 'Channels refreshed.')

@bot.on(events.NewMessage)
async def handle_user_response(event):
    chat_id = event.chat_id
    if chat_id in user_responses:
        action = user_responses[chat_id]['action']
        user_responses.pop(chat_id, None)  # Clear the action after processing
        text = event.message.message

        data = load_data()

        if action == 'add_channel':
            try:
                channel_id = int(text)
                if channel_id not in data['target_channels']:
                    data['target_channels'].append(channel_id)
                    save_data(data)
                    await bot.send_message(chat_id, f'Channel {channel_id} added.')
                else:
                    await bot.send_message(chat_id, f'Channel {channel_id} is already added.')
            except ValueError:
                await bot.send_message(chat_id, 'Invalid channel ID. Please send a numeric ID.')

        elif action == 'remove_channel':
            try:
                channel_id = int(text)
                if channel_id in data['target_channels']:
                    data['target_channels'].remove(channel_id)
                    save_data(data)
                    await bot.send_message(chat_id, f'Channel {channel_id} removed.')
                else:
                    await bot.send_message(chat_id, f'Channel {channel_id} not found.')
            except ValueError:
                await bot.send_message(chat_id, 'Invalid channel ID. Please send a numeric ID.')

client.start()
client.run_until_disconnected()

