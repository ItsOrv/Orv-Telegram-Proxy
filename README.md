
# Orv-Telegram-Proxy

This project is a Python-based Telegram bot that uses the `Telethon` library to scrape Telegram proxy links from specific Telegram groups and channels and send them in an organized format through a Telegram bot.

## Features
- **Scrapes Proxy Links:** The bot monitors specific Telegram channels for proxy links via telegram account.
- **Extracts Proxy Information:** The bot extracts the IP address, port, and geographical location of the proxy server.
- **Sends Proxies via Bot:** The bot formats and sends the extracted proxy information via a Telegram bot, including buttons for quick connection.
- **Manage Channels:** Admins can add or remove channels directly through Telegram bot commands.

## Installation

To set up and run the project using Docker, follow these steps:

1. **Run the setup script:**

   ```bash
   bash <(curl -s https://raw.githubusercontent.com/ItsOrv/Orv-Telegram-Proxy/main/setup.sh)
   ```

   This command will:
   - Clone the repository if it's not already present.
   - Create necessary files and directories.
   - Build and start Docker containers.

2. **Set Up Environment Variables:**

   The `setup.sh` script will automatically create a `.env` file for Docker with placeholder values. Please edit `.env` with your actual API credentials:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   ADMIN_ID=your_admin_id
   ```

3. **Docker Configuration:**

   The `setup.sh` script will generate a `Dockerfile` and `docker-compose.yml` for containerization. 

   **Dockerfile** - Configures the Python environment and application.

   **docker-compose.yml** - Defines the Docker service and environment variables.

4. **Start Docker Containers:**

   If you need to restart or rebuild the Docker containers manually, use:

   ```bash
   docker-compose up --build -d
   ```

## Usage

1. **Access the Bot:**
   - Start a conversation with your bot on Telegram.
   - Use the `/start` command to display management options.

2. **Manage Channels:**
   - **Add Channel:** Click "Add Channel" and send the channel ID.
   - **Remove Channel:** Click "Remove Channel" and send the channel ID.
   - **Refresh Channels:** Click "Refresh Channels" to update the list of channels.

3. **Run the Bot:**

   If you are running the bot outside of Docker, use:

   ```bash
   python3 src/bot.py
   ```

   The bot will start monitoring for proxy links.

