import asyncio
import threading
from gevent import monkey
monkey.patch_all()  # پچ کردن کتابخانه‌ها برای همزمانی
from flask import Flask
from telethon import TelegramClient
from bot import bot, client  # Assuming the bot and client are initialized in bot.py
import gevent

app = Flask(__name__)

# Function to run the Flask app in a separate thread using gevent
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True)

async def main():
    # Ensure full connection for Telethon client
    await client.start()

    # Start Flask app in a separate gevent greenlet
    gevent.spawn(run_flask)

    # Schedule the cleaning task (can run in the background)
    asyncio.create_task(schedule_cleaning())

    # Run the bot
    await client.run_until_disconnected()

# Start the main asynchronous function
asyncio.run(main())
