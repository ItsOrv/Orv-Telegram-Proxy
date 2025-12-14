# config.py

import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


def get_required_env(key: str) -> str:
    """Get required environment variable or raise error."""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable {key} is not set. Please check your .env file.")
    return value


def get_optional_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get optional environment variable with default value."""
    return os.getenv(key, default)


# Required configuration
api_id: str = get_required_env('API_ID')
api_hash: str = get_required_env('API_HASH')
bot_token: str = get_required_env('BOT_TOKEN')
channel_id: str = get_required_env('CHANNEL_ID')

# Optional URLs (can be None)
proxy_channel_url: Optional[str] = get_optional_env('PROXY_CHANNEL_URL')
config_channel_url: Optional[str] = get_optional_env('CONFIG_CHANNEL_URL')
bot_url: Optional[str] = get_optional_env('BOT_URL')
support_url: Optional[str] = get_optional_env('SUPPORT_URL')

# Load channels as a list of integers
channels_str = get_required_env('CHANNELS')
channels: List[int] = [int(chat_id.strip()) for chat_id in channels_str.split(',') if chat_id.strip()]
