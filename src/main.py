"""
Main entry point for running both the Telegram bot and Flask web server.
"""

import asyncio
import threading
import logging
from logging_config import setup_logging

# Setup logging first, before importing other modules
setup_logging()

from bot import bot, client, schedule_cleaning, executor
from config import bot_token

logger = logging.getLogger(__name__)

# Import Flask app from app.py
from app import app


def run_flask_app() -> None:
    """Run Flask app in a separate thread."""
    try:
        logger.info("Starting Flask web server on http://0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except OSError as e:
        # Handle port already in use or permission errors
        if "Address already in use" in str(e) or "Permission denied" in str(e):
            logger.error(f"Cannot start Flask server: {e}. Port 5000 may be in use.")
        else:
            logger.error(f"OS error running Flask app: {e}")
    except Exception as e:
        logger.error(f"Error running Flask app: {e}", exc_info=True)


async def main() -> None:
    """Main async function to start bot and Flask server."""
    try:
        # Ensure full connection for Telethon client
        await client.start()
        logger.info("Telegram client started successfully")
        
        # Start the bot client (for sending messages)
        await bot.start(bot_token=bot_token)
        logger.info("Telegram bot client started successfully")
        
        # Schedule the cleaning task
        asyncio.create_task(schedule_cleaning())
        logger.info("Scheduled proxy cleaning task")
        
        # Start Flask app in a separate thread
        flask_thread = threading.Thread(target=run_flask_app, daemon=True)
        flask_thread.start()
        logger.info("Flask web server thread started")
        
        # Run the bot (this will block until disconnected)
        logger.info("Bot is running and listening for messages...")
        await client.run_until_disconnected()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        raise
    finally:
        # Cleanup connections
        try:
            await bot.disconnect()
            await client.disconnect()
            # Shutdown executor
            executor.shutdown(wait=True)
            logger.info("Resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application shutdown complete")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
