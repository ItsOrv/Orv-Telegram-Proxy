# Orv Telegram Proxy

Automated Telegram bot for collecting, validating, and forwarding proxy links with geolocation detection and performance testing.

[Telegram Channel](https://t.me/Orv_Proxy)

## Overview

This project provides a production-ready Telegram bot that monitors specified channels for proxy links, validates them through ping testing, identifies their geographic location, and forwards formatted messages to your channel. The bot includes a Flask web interface for viewing collected proxies and implements robust error handling, rate limiting, and thread-safe operations.

## Features

- **Automatic Proxy Collection**: Monitors multiple Telegram channels/groups for proxy links in real-time
- **Geolocation Detection**: Identifies proxy server country using IP geolocation API with hostname resolution support
- **Performance Testing**: Tests proxy connectivity and measures ping latency before forwarding
- **Web Interface**: Flask-based web server displays collected proxies with filtering and search capabilities
- **Automatic Cleanup**: Removes proxies older than 24 hours to maintain data freshness
- **Rate Limiting**: Implements API rate limiting to respect external service limits
- **Thread-Safe Operations**: Atomic file operations prevent data corruption in concurrent scenarios
- **Input Validation**: Comprehensive validation for proxy links, IP addresses, and ports
- **Error Handling**: Robust error handling with detailed logging for debugging

## Requirements

- Python 3.9 or higher
- Telegram account with API credentials
- Telegram bot token
- Access to channels/groups for proxy collection

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ItsOrv/Orv-Telegram-Proxy.git
cd Orv-Telegram-Proxy
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Required
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
CHANNEL_ID=your_channel_id
CHANNELS=1111111,2222222,3333333

# Optional (for message formatting)
PROXY_CHANNEL_URL=https://t.me/your_channel
CONFIG_CHANNEL_URL=https://t.me/your_config_channel
BOT_URL=https://t.me/your_bot
SUPPORT_URL=https://t.me/your_support
```

## Configuration

### Required Variables

- `API_ID`: Your Telegram API ID from [my.telegram.org](https://my.telegram.org)
- `API_HASH`: Your Telegram API hash
- `BOT_TOKEN`: Bot token from [@BotFather](https://t.me/BotFather)
- `CHANNEL_ID`: Target channel ID where proxy messages will be sent
- `CHANNELS`: Comma-separated list of channel/group IDs to monitor (your account must be a member)

### Optional Variables

- `PROXY_CHANNEL_URL`: Proxy channel URL for message buttons
- `CONFIG_CHANNEL_URL`: Configuration channel URL
- `BOT_URL`: Bot URL for message buttons
- `SUPPORT_URL`: Support channel URL

## Usage

### Start the bot

Run the main entry point to start both the bot and web server:

```bash
python3 src/main.py
```

The bot will:
1. Prompt for phone number authentication (first run only)
2. Start monitoring specified channels for proxy links
3. Process and validate each proxy (ping test, geolocation)
4. Forward formatted messages to your channel
5. Start Flask web server on `http://localhost:5000`

### Bot-only mode

To run only the bot without the web interface:

```bash
python3 src/bot.py
```

### Web interface

Access the web interface at `http://localhost:5000` to view collected proxies. The interface provides:
- List of all collected proxies
- Country information
- Ping latency data
- Direct connection buttons

## Architecture

### Components

- **bot.py**: Core bot logic with async message processing, proxy validation, and geolocation
- **app.py**: Flask web server for proxy display
- **main.py**: Entry point that orchestrates bot and web server
- **config.py**: Environment variable management with validation
- **logging_config.py**: Centralized logging configuration

### Technical Details

- **Async/Await**: Non-blocking I/O operations for optimal performance
- **Thread Pool Executor**: Handles CPU-bound operations (socket connections)
- **File Locking**: Thread-safe JSON file operations
- **Rate Limiting**: Semaphore-based concurrency control and time-based rate limiting
- **Input Sanitization**: Markdown escaping and input validation prevent injection attacks

## Project Structure

```
Orv-Telegram-Proxy/
├── src/
│   ├── bot.py              # Main bot logic
│   ├── app.py              # Flask web application
│   ├── main.py             # Entry point
│   ├── config.py           # Configuration management
│   ├── logging_config.py   # Logging setup
│   └── templates/
│       └── index.html      # Web interface template
├── proxies.json            # Proxy storage (auto-generated)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md
```

## Error Handling

The bot implements comprehensive error handling:

- Network errors are logged and retried where appropriate
- Invalid proxy links are skipped with detailed logging
- API rate limits are respected with automatic throttling
- File operation errors are caught and handled gracefully
- Connection failures trigger automatic reconnection

Check console output or log files for detailed error information.

## Security

- Input validation for all proxy links and parameters
- Markdown injection prevention through proper escaping
- Thread-safe file operations prevent race conditions
- Rate limiting prevents API abuse
- Secure handling of sensitive credentials via environment variables

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Submit a pull request with a clear description

For major changes, please open an issue first to discuss proposed modifications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please open an issue on GitHub or contact through the Telegram channel.
