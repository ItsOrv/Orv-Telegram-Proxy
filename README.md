# Orv Telegram Proxy

Telegram bot that collects proxy links from channels, checks them and forwards them to your own channel.

[Telegram Channel](https://t.me/Orv_Proxy)

## Features

- Watches one or more channels for proxy links
- Detects the country of each proxy from its IP
- Pings the proxy and shows the latency
- Forwards a formatted message with a connect button

## Setup

```bash
git clone https://github.com/ItsOrv/Orv-Telegram-Proxy.git
cd Orv-Telegram-Proxy
pip install -r requirements.txt
```

Run the setup script to create your `.env`:

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
python src/bot.py
```

On the first run you will be asked for your phone number to log in.

## License

MIT
