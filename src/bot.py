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
from urllib.parse import quote
import ipaddress
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

# Initialize client and bot
# Note: bot will be started in main() function to ensure proper async initialization
client = TelegramClient('session_name', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash)


def _ping_proxy_sync(host: str, port: str, timeout: float = 3.0) -> Optional[float]:
    """
    Synchronous ping implementation (runs in thread pool).
    
    Args:
        host: The proxy server hostname or IP address
        port: The proxy server port
        timeout: Connection timeout in seconds
        
    Returns:
        Ping time in milliseconds if successful, None otherwise
    """
    try:
        port_int = int(port)
        start_time = time.time()
        # Use context manager to ensure socket is always closed
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port_int))
        
        if result == 0:
            ping_ms = (time.time() - start_time) * 1000
            return round(ping_ms, 2)
        return None
    except (socket.gaierror, socket.timeout, ValueError, OSError) as e:
        logger.debug(f"Ping failed for {host}:{port} - {e}")
        return None


async def ping_proxy(host: str, port: str, timeout: float = 3.0) -> Optional[float]:
    """
    Ping a proxy server by attempting to connect to it (non-blocking).
    
    Args:
        host: The proxy server hostname or IP address
        port: The proxy server port
        timeout: Connection timeout in seconds
        
    Returns:
        Ping time in milliseconds if successful, None otherwise
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _ping_proxy_sync, host, port, timeout)


async def get_country_from_ip(ip: str, timeout: float = 5.0) -> str:
    """
    Get country information for an IP address using ip-api.com (non-blocking).
    
    Args:
        ip: IP address to look up (validated before calling)
        timeout: Request timeout in seconds
        
    Returns:
        Country name or 'Unknown' if lookup fails
    """
    try:
        # Additional validation before making request
        if not ip or len(ip) > 45:  # Max IPv6 length
            return 'Unknown'
        
        # Sanitize IP for URL (basic check)
        if any(char in ip for char in ['\n', '\r', '\t', ' ', '<', '>', '&']):
            logger.warning(f"Invalid characters in IP address: {ip}")
            return 'Unknown'
        
        # Use proper URL encoding
        encoded_ip = quote(ip, safe='')
        url = f'http://ip-api.com/json/{encoded_ip}'
        
        # Use aiohttp for async HTTP requests
        timeout_obj = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout_obj) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
        
        # Validate response
        if data.get('status') == 'fail':
            logger.warning(f"IP API returned error: {data.get('message', 'Unknown error')}")
            return 'Unknown'
        
        country = data.get('country', 'Unknown')
        # Sanitize country name (basic check)
        if country and len(country) <= 100:  # Reasonable country name length
            return country
        return 'Unknown'
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching country for {ip}: {e}")
        return 'Unknown'
    except Exception as e:
        logger.error(f"Unexpected error getting country for {ip}: {e}")
        return 'Unknown'


def load_proxies() -> Dict:
    """
    Load proxies from the JSON file in a thread-safe manner.
    
    Returns:
        Dictionary of proxies or empty dict if file doesn't exist or is invalid
    """
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
    """
    Save proxies to the JSON file in a thread-safe manner.
    
    Args:
        proxies: Dictionary of proxies to save
    """
    with file_lock:
        try:
            # Create backup before writing
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
    """
    Check if the proxy has been logged in the proxy file.
    
    Args:
        proxy_link: The proxy link to check
        
    Returns:
        True if proxy is already logged, False otherwise
    """
    proxies = load_proxies()
    return any(entry.get('link') == proxy_link for entry in proxies.values())


def log_proxy(proxy_link: str, country: str, ip: str, port: str, ping: Optional[float] = None) -> None:
    """
    Log the proxy to the JSON file.
    
    Args:
        proxy_link: The full proxy link
        country: Country name
        ip: IP address
        port: Port number
        ping: Optional ping time in milliseconds
    """
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
    """
    Validate if a string is a valid IP address (IPv4 or IPv6).
    
    Args:
        ip: String to validate
        
    Returns:
        True if valid IP address, False otherwise
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_port(port: str) -> bool:
    """
    Validate if a string is a valid port number (1-65535).
    
    Args:
        port: String to validate
        
    Returns:
        True if valid port, False otherwise
    """
    try:
        port_int = int(port)
        return 1 <= port_int <= 65535
    except ValueError:
        return False


def parse_proxy_link(link: str) -> Optional[Tuple[str, str]]:
    """
    Parse a Telegram proxy link to extract server and port with validation.
    
    Args:
        link: The proxy link to parse
        
    Returns:
        Tuple of (server, port) if successful, None otherwise
    """
    try:
        # Validate link format
        if not link or len(link) > 500:  # Reasonable length limit
            return None
        
        server_match = re.search(r'server=([^&]+)', link)
        port_match = re.search(r'port=([^&]+)', link)
        
        if not server_match or not port_match:
            return None
        
        server = server_match.group(1).strip()
        port = port_match.group(1).strip()
        
        # Basic validation
        if not server or not port:
            return None
        
        # Validate port
        if not validate_port(port):
            logger.warning(f"Invalid port number: {port}")
            return None
        
        # Validate IP address (server can be IP or hostname)
        # For hostnames, we'll do basic validation (no spaces, reasonable length)
        if not server or len(server) > 253:  # Max hostname length
            return None
        
        # Check for potentially malicious characters
        if any(char in server for char in ['\n', '\r', '\t', ' ', '<', '>']):
            return None
        
        return (server, port)
    except Exception as e:
        logger.error(f"Error parsing proxy link {link}: {e}")
        return None


def escape_markdown(text: str) -> str:
    """
    Escape special characters for Telegram markdown v2.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text safe for Telegram markdown
    """
    # Telegram markdown v2 special characters that need escaping
    special_chars = ['*', '_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    escaped = text
    for char in special_chars:
        escaped = escaped.replace(char, f'\\{char}')
    return escaped


def format_proxy_message(
    country: str,
    ip: str,
    port: str,
    ping: Optional[float] = None
) -> str:
    """
    Format the proxy message for Telegram.
    
    Args:
        country: Country name
        ip: IP address (may be truncated)
        port: Port number
        ping: Optional ping time in milliseconds
        
    Returns:
        Formatted message string
    """
    # Escape country name to prevent markdown injection
    safe_country = escape_markdown(country)
    
    # Truncate IP if too long
    display_ip = ip
    if len(ip) > 16:
        display_ip = ip[:16] + '.etc'
    
    # Escape IP and port for safety
    safe_ip = escape_markdown(display_ip)
    safe_port = escape_markdown(port)
    
    message_parts = [
        "**\u2774Orv\u2774**\n",
        f"\u2022 Country: {safe_country}\n",
        f"\u2022 IP: {safe_ip}\n",
        f"\u2022 Port: {safe_port}\n"
    ]
    
    if ping is not None:
        # Ping is a number, but escape it for consistency
        safe_ping = escape_markdown(f"{ping}ms")
        message_parts.append(f"\u2022 Ping: {safe_ping}\n")
    
    message_parts.append("\n")
    
    # Add optional links
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
    # Use a more restrictive regex to prevent ReDoS attacks
    # Limit the character class and use non-greedy matching
    proxy_links = re.findall(r'https?://t\.me/proxy\?[^\s<>"]{1,500}', message)
    
    if not proxy_links:
        return
    
    for link in proxy_links:
        try:
            # Parse proxy link
            parsed = parse_proxy_link(link)
            if not parsed:
                logger.warning(f"Failed to parse proxy link: {link}")
                continue
            
            server, port = parsed
            
            # Check if proxy is already logged
            if is_proxy_logged(link):
                logger.info(f"Proxy {link} has already been processed.")
                continue
            
            # Get country information
            country = await get_country_from_ip(server)
            
            # Ping the proxy server
            ping = await ping_proxy(server, port)
            if ping is None:
                logger.warning(f"Could not ping proxy {server}:{port}")
                # Continue anyway, but don't include ping in message
            
            # Format and send message
            text = format_proxy_message(country, server, port, ping)
            buttons = [Button.url('Connect', link)]
            
            try:
                # Ensure bot is connected before sending
                if not bot.is_connected():
                    logger.warning("Bot client is not connected, skipping message send")
                    continue
                
                # Validate channel_id before sending
                if not channel_id or not str(channel_id).strip():
                    logger.error("Invalid channel_id: cannot be empty")
                    continue
                
                await bot.send_message(
                    channel_id,
                    text,
                    buttons=buttons,
                    link_preview=False
                )
                logger.info(f"Successfully sent proxy {server}:{port} to channel")
            except ValueError as e:
                logger.error(f"Invalid channel_id format: {e}")
                continue
            except Exception as e:
                logger.error(f"Error sending message to channel {channel_id}: {e}", exc_info=True)
                continue
            
            # Log the proxy
            log_proxy(link, country, server, port, ping)
            
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
            await asyncio.sleep(86400)  # Sleep for 24 hours
            await clean_old_proxies()
        except Exception as e:
            logger.error(f"Error in cleaning schedule: {e}")
            await asyncio.sleep(3600)  # Retry after 1 hour on error


# Note: main() function has been moved to main.py to avoid duplication
# This module can still be run standalone for testing purposes
if __name__ == '__main__':
    import sys
    logger.warning("Running bot.py directly is deprecated. Please use 'python src/main.py' instead.")
    logger.warning("For standalone bot (without web server), consider creating a separate entry point.")
    sys.exit(1)
