# Orv Telegram Proxy

This project is a Telegram bot designed to collect proxy links from specific Telegram channels and send them to your channel. The bot also retrieves the country of the proxy server using the IP address and formats the message accordingly.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automatic Proxy Collection**: The bot monitors specified channels for proxy links.
- **Country Identification**: The bot fetches the country information based on the IP address of the proxy.
- **Customizable Messages**: The bot formats and sends messages to a designated channel with proxy information and connect button.
- **Error Handling**: The bot includes logging and error handling to manage exceptions and provide meaningful error messages.

## Requirements

- Python 3.7+
- Telegram account
- Telegram bot token
- Channels from which to collect proxy links

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ItsOrv/Orv-Telegram-Proxy.git
   cd Orv-Telegram-Proxy
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
   On Windows use:
   ```bash
   python3 -m venv venv
   venv\Scripts\activate
   ```
   
4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory of the project with the following content:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   CHANNEL_ID=your_channel_id
   
   PROXY_CHANNEL_URL=https://....
   CONFIG_CHANNEL_URL=https://....
   BOT_URL=https://....
   SUPPORT_URL=https://....
   
   CHANNELS=1111111,2222222,3333333


   ```

## Configuration

- **api_id**: Your Telegram API ID.
- **api_hash**: Your Telegram API hash.
- **bot_token**: The token of your Telegram bot.
- **channel_id**: The ID of the Telegram channel where the bot will send proxy messages.

you can simply delete these urls from code:

- **proxy_channel_url**: URL of the proxy channel (for inclusion in messages).
- **config_channel_url**: URL of my vpn channel (for inclusion in messages).
- **bot_url**: URL of the bot (for inclusion in messages).
- **support_url**: URL of the support (for inclusion in messages).
- **channels**: Numeric id of groups or channels for proxy search, the desired account must be a member of the channels or groups

## Running the Bot

1. Ensure that the `.env` file is correctly configured.
2. Run the bot:

   ```bash
   python3 src/bot.py
   ```
   
The bot will start listening to the specified channels for new proxy links and forward them to your channel.

## Error Handling

- The bot uses logging to capture and report errors.
- Common errors like network issues, missing data, or incorrect configuration are logged for easier debugging.
- If any unexpected issues occur, check the console output or the log files.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
