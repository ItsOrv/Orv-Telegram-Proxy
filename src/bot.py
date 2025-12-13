"""
Telegram bot for collecting and forwarding proxy links with country detection and ping testing.
"""

from telethon import TelegramClient, events, Button
from config import (
    api_id, api_hash, bot_token, channels, proxy_channel_url,
    config_channel_url, bot_url, support_url, channel_id
)
import aiohttp
import re
import logging
import os
import asyncio
import json
import socket
import time
from typing import Dict, Optional, Tuple
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

# Setup logging (centralized configuration)
from logging_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

# File to store proxies - use absolute path based on script location
_script_dir = os.path.dirname(os.path.abspath(__file__))
PROXY_FILE = os.path.join(os.path.dirname(_script_dir), 'proxies.json')
# File lock for thread-safe operations
file_lock = Lock()
# Thread pool executor for blocking I/O operations
executor = ThreadPoolExecutor(max_workers=4)

# Rate limiting for IP geolocation API (ip-api.com free tier: 45 requests/minute)
# Use semaphore to limit concurrent requests
api_semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent API requests
# Simple rate limiter: track last request time
_last_api_request_time = 0.0
_api_min_interval = 1.4  # ~43 requests per minute (slightly under 45 to be safe)

# Initialize client and bot
# Note: bot will be started in main() function to ensure proper async initialization
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash)


def _ping_proxy_sync(host: str, port: str, timeout: float = 3.0) -> Optional[float]:
    """Synchronous ping implementation (runs in thread pool)."""
    try:
        port_int = int(port)
        start_time = time.time()
        # Use context manager to ensure socket is always closed
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port_int))
        if result == 0:
            return round((time.time() - start_time) * 1000, 2)
        return None
    except (socket.gaierror, socket.timeout, ValueError, OSError) as e:
        logger.debug(f"Ping failed for {host}:{port} - {e}")
        return None


async def ping_proxy(host: str, port: str, timeout: float = 3.0) -> Optional[float]:
    """Ping a proxy server by attempting to connect to it (non-blocking)."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _ping_proxy_sync, host, port, timeout)


async def get_country_from_ip(ip: str, timeout: float = 5.0) -> str:
    """Get country information for an IP address using ip-api.com (non-blocking)."""
    try:
        url = f'http://ip-api.com/json/{ip}'
        timeout_obj = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout_obj) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
        if data.get('status') == 'fail':
            logger.warning(f"IP API returned error: {data.get('message', 'Unknown error')}")
            return 'Unknown'
        return data.get('country', 'Unknown')
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching country for {ip}: {e}")
        return 'Unknown'
    except Exception as e:
        logger.error(f"Unexpected error getting country for {ip}: {e}")
        return 'Unknown'


def load_proxies() -> Dict:
    """Load proxies from the JSON file in a thread-safe manner."""
    with file_lock:
        if not os.path.exists(PROXY_FILE):
            return {}
        try:
            with open(PROXY_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading proxies file: {e}")
            return {}


def save_proxies(proxies: Dict) -> None:
    """Save proxies to the JSON file in a thread-safe manner."""
    with file_lock:
        try:
            if os.path.exists(PROXY_FILE):
                backup_file = f"{PROXY_FILE}.bak"
                with open(PROXY_FILE, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
            with open(PROXY_FILE, 'w', encoding='utf-8') as file:
                json.dump(proxies, file, indent=4, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Error saving proxies file: {e}")


def is_proxy_logged(proxy_link: str) -> bool:
    """Check if the proxy has been logged in the proxy file."""
    proxies = load_proxies()
    return any(entry.get('link') == proxy_link for entry in proxies.values())


def log_proxy(proxy_link: str, country: str, ip: str, port: str, ping: Optional[float] = None) -> None:
    """Log the proxy to the JSON file."""
    proxies = load_proxies()
    proxy_id = str(len(proxies) + 1)
    proxy_data = {
        'link': proxy_link,
        'Country': country,
        'IP': ip,
        'Port': port
    }
    if ping is not None:
        proxy_data['Ping'] = f"{ping}ms"
    proxies[proxy_id] = proxy_data
    save_proxies(proxies)


def validate_ip_address(ip: str) -> bool:
    """Validate if a string is a valid IP address (IPv4 or IPv6)."""
    import ipaddress
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_port(port: str) -> bool:
    """Validate if a string is a valid port number (1-65535)."""
    try:
        port_int = int(port)
        return 1 <= port_int <= 65535
    except ValueError:
        return False


def parse_proxy_link(link: str) -> Optional[Tuple[str, str]]:
    """Parse a Telegram proxy link to extract server and port with validation."""
    try:
        if not link or len(link) > 500:
            return None
        server_match = re.search(r'server=([^&]+)', link)
        port_match = re.search(r'port=([^&]+)', link)
        if not server_match or not port_match:
            return None
        server = server_match.group(1).strip()
        port = port_match.group(1).strip()
        if not server or not port:
            return None
        if not validate_port(port):
            logger.warning(f"Invalid port number: {port}")
            return None
        if not server or len(server) > 253:
            return None
        return (server, port)
    except Exception as e:
        logger.error(f"Error parsing proxy link {link}: {e}")
        return None


def escape_markdown(text: str) -> str:
    """Escape special characters for Telegram markdown v2."""
    special_chars = ['*', '_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    escaped = text
    for char in special_chars:
        escaped = escaped.replace(char, f'\\{char}')
    return escaped


def format_proxy_message(country: str, ip: str, port: str, ping: Optional[float] = None) -> str:
    """Format the proxy message for Telegram."""
    safe_country = escape_markdown(country)
    display_ip = ip
    if len(ip) > 16:
        display_ip = ip[:16] + '.etc'
    safe_ip = escape_markdown(display_ip)
    safe_port = escape_markdown(port)

    message_parts = [
        "**❴Orv❴**\n",
        f"• Country: {safe_country}\n",
        f"• IP: {safe_ip}\n",
        f"• Port: {safe_port}\n"
    ]
    if ping is not None:
        safe_ping = escape_markdown(f"{ping}ms")
        message_parts.append(f"• Ping: {safe_ping}\n")
    message_parts.append("\n")

    link_parts = []
    if proxy_channel_url:
        link_parts.append(f"[proxy]({proxy_channel_url})")
    if config_channel_url:
        link_parts.append(f"[config]({config_channel_url})")
    if bot_url:
        link_parts.append(f"[bot]({bot_url})")
    if support_url:
        link_parts.append(f"[support]({support_url})")
    if link_parts:
        message_parts.append("~".join(link_parts))

    return "".join(message_parts)


@client.on(events.NewMessage(chats=channels))
async def my_event_handler(event):
    """Handle new messages from monitored channels."""
    if not event.message or not event.message.message:
        return
    message = event.message.message
    proxy_links = re.findall(r'https?://t\.me/proxy\?\S+', message)
    if not proxy_links:
        return
    for link in proxy_links:
        try:
            parsed = parse_proxy_link(link)
            if not parsed:
                logger.warning(f"Failed to parse proxy link: {link}")
                continue
            server, port = parsed

            if is_proxy_logged(link):
                logger.info(f"Proxy {link} has already been processed.")
                continue

            country = await get_country_from_ip(server)
            ping = await ping_proxy(server, port)
            if ping is None:
                logger.warning(f"Could not ping proxy {server}:{port}")

            log_proxy(link, country, server, port, ping)

            text = format_proxy_message(country, server, port, ping)
            buttons = [Button.url('Connect', link)]
            await bot.send_message(channel_id, text, buttons=buttons, link_preview=False)
        except AttributeError as e:
            logger.error(f"Error parsing link: {link}. Required parameters missing: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing proxy {link}: {e}", exc_info=True)


async def clean_old_proxies() -> None:
    """Clear the proxy file (called periodically)."""
    try:
        if os.path.exists(PROXY_FILE):
            with file_lock:
                with open(PROXY_FILE, 'w', encoding='utf-8') as file:
                    json.dump({}, file, indent=4)
            logger.info("Cleaned old proxies file")
    except Exception as e:
        logger.error(f"Error cleaning proxies file: {e}")


async def schedule_cleaning() -> None:
    """Schedule the cleaning task every 24 hours."""
    while True:
        try:
            await asyncio.sleep(86400)
            await clean_old_proxies()
        except Exception as e:
            logger.error(f"Error in cleaning schedule: {e}")
            await asyncio.sleep(3600)


if __name__ == '__main__':
    import sys
    logger.warning("Running bot.py directly is deprecated. Please use 'python src/main.py' instead.")
    sys.exit(1)
