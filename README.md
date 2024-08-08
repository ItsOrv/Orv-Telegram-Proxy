# Telegram Proxy Scraper and Sender

This project is a Python-based Telegram bot that uses the `Telethon` library to scrape Telegram proxy links from specific Telegram groups and channels and send them in an organized format through a Telegram bot.

## Features
- **Scrapes Proxy Links:** The bot monitors specific Telegram channels for proxy links.
- **Extracts Proxy Information:** The bot extracts the IP address, port, and geographical location of the proxy server.
- **Sends Proxies via Bot:** The bot formats and sends the extracted proxy information via a Telegram bot, including buttons for quick connection.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/telegram-proxy-scraper.git
   cd telegram-proxy-scraper
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create and configure your `.env` file with your API credentials:

   ```bash
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   ```

## Usage

1. **Run the script:**

   ```bash
   python3 bot.py
   ```

2. The bot will start monitoring the specified Telegram channels for proxy links.

## Acknowledgements

- The project uses the [Telethon](https://github.com/LonamiWebs/Telethon) library for interacting with the Telegram API.
- IP location data is retrieved using the [IP-API](http://ip-api.com/).

Feel free to contribute or suggest improvements by opening an issue or pull request on GitHub!
