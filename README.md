# Orv Telegram Proxy

Telegram bot that automatically collects proxy links from channels, validates them and forwards them to your own channel.

[Join our Telegram channel](https://t.me/Orv_Proxy)

## Features

- Watches one or more channels for new proxy links
- Detects the country of each proxy from its IP
- Pings the proxy and shows the latency
- Forwards a formatted message with a connect button

## Setup

```bash
git clone https://github.com/ItsOrv/Orv-Telegram-Proxy.git
cd Orv-Telegram-Proxy
pip install -r requirements.txt
```

Run the helper script to create your `.env`:

```bash
bash setup.sh
```

Or create the `.env` file yourself:

```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
CHANNEL_ID=your_channel_id
CHANNELS=1111111,2222222
```

## Usage

```bash
python3 src/bot.py  # starts the bot
```

On the first run you will be prompted for your phone number to authenticate.

## License

MIT

## Requirements

- Python 3.9+
- A Telegram account and a bot token from BotFather

### Monitored channels

Set `CHANNELS` to a comma separated list of channel ids your account is a member of.

Make sure your account has joined the channels listed in `CHANNELS`.

Each forwarded proxy includes its measured ping and detected country.

## Support

Open an issue or reach out through the Telegram channel.

On the first run Telethon will ask for your phone number to log in.

## Web interface

Run `python src/app.py` and open http://localhost:5000 to see the collected proxies.

The web page refreshes the list from `proxies.json` on each request.

## Notes

Logging is configured centrally in `logging_config.py`.

The bot, web app and config are being split into separate modules under `src/`.
