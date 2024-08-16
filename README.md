
# Orv-Telegram-Proxy

This project is a Python-based Telegram bot that uses the `Telethon` library to scrape Telegram proxy links from specific Telegram groups and channels and send them in an organized format through a Telegram bot.

## Features
- **Scrapes Proxy Links:** The bot monitors specific Telegram channels for proxy links via telegram account.
- **Extracts Proxy Information:** The bot extracts the IP address, port, and geographical location of the proxy server.
- **Sends Proxies via Bot:** The bot formats and sends the extracted proxy information via a Telegram bot, including buttons for quick connection.

## Installation

1. create `.env` file:
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   ADMIN_ID=your_admin_id
   ```

2. run main file:
   ```
   python3 bot.py
   ```
   

**to-do list**
1. - **Manage Channels:** Admins can add or remove channels directly through Telegram bot commands.
