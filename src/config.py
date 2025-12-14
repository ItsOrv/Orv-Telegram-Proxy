# config.py

import os
import logging
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# Get logger (logging will be configured by logging_config module when imported)
logger = logging.getLogger(__name__)


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

# Validate channels list is not empty
if not channels:
    raise ValueError(
        "CHANNELS environment variable must contain at least one valid channel ID. "
        "Format: CHANNELS=1111111,2222222,3333333"
    )

# Validate channel_id format (can be integer or string starting with -100 for supergroups)
try:
    # Try to convert to int to validate format
    channel_id_int = int(channel_id)
    if channel_id_int == 0:
        raise ValueError("CHANNEL_ID cannot be zero")
except ValueError:
    # If not a valid integer, check if it's a valid string format
    if not channel_id or not channel_id.strip():
        raise ValueError("CHANNEL_ID cannot be empty")
    # Allow string format for channel usernames (e.g., @channelname)
    if not (channel_id.startswith('@') or channel_id.startswith('-100')):
        logger.warning(
            f"CHANNEL_ID '{channel_id}' may not be in the correct format. "
            "Expected: integer, @username, or -100XXXXXXXXX format"
        )
