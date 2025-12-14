"""
Main entry point for running both the Telegram bot and Flask web server.
"""

import asyncio
import threading
import logging

from bot import bot, client, schedule_cleaning
from config import bot_token
from app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_flask_app():
    """Run Flask app in a separate thread."""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


async def main():
    """Main async function to start bot and Flask server."""
    await client.start()
    await bot.start(bot_token=bot_token)
    asyncio.create_task(schedule_cleaning())

    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()

    logger.info("Bot is running and listening for messages...")
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
