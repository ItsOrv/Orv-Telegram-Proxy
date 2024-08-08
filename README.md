
# Orv Telegram Proxy

This project is a Python-based Telegram bot that uses the `Telethon` library to scrape Telegram proxy links from specific Telegram groups and channels and send them in an organized format through a Telegram bot.

## Features
- **Scrapes Proxy Links:** The telegram account monitors for proxy links.
- **Extracts Proxy Information:** The bot extracts the IP address, port, and geographical location of the proxy server.
- **Sends Proxies via Bot:** The bot formats and sends the extracted proxy information via a Telegram bot, including buttons for quick connection.

## Installation

To set up the project and install all dependencies, simply run the following command:

```bash
bash <(curl -s https://raw.githubusercontent.com/ItsOrv/Orv-Telegram-Proxy/main/setup.sh)
```

This command will:
1. Clone the repository.
2. Navigate into the project directory.
3. Create and activate a virtual environment.
4. Install the required Python packages.
5. Prompt you for necessary API credentials and create the `.env` file.

## Usage

1. **Activate the virtual environment:**

   ```bash
   source venv/bin/activate
   ```

2. **Run the bot:**

   ```bash
   python src/bot.py
   ```
   
## Acknowledgements

- The project uses the [Telethon](https://github.com/LonamiWebs/Telethon) library for interacting with the Telegram API.
- IP location data is retrieved using the [IP-API](http://ip-api.com/).

Feel free to contribute or suggest improvements by opening an issue or pull request on GitHub!
