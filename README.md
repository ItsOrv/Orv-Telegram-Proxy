# Orv Telegram Proxy

Telegram bot that grabs proxy links from channels and forwards them to your own channel.

## Setup

```bash
pip install -r requirements.txt
python bot.py
```

Fill in your api_id, api_hash and bot_token at the top of bot.py before running.

## Example

Send a proxy link to a watched channel and the bot reposts it with a Connect button.

## Notes

This is a hobby project, expect rough edges.


## Features

- Watches channels for proxy links
- Detects proxy country from its IP
- Forwards a formated message with a connect button
