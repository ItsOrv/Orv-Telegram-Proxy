"""
Flask web application for displaying proxy information.
"""

from flask import Flask, render_template
import json
import os
import logging
from typing import Dict
from logging_config import setup_logging

# Setup logging
setup_logging()

from config import (
    proxy_channel_url, config_channel_url, bot_url, support_url
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
# Use absolute path for proxy file (same location as bot.py uses)
_script_dir = os.path.dirname(os.path.abspath(__file__))
PROXY_FILE = os.path.join(os.path.dirname(_script_dir), 'proxies.json')


def load_proxies() -> Dict:
    """
    Load proxies from the JSON file (read-only, no locking needed for Flask).
    
    Returns:
        Dictionary of proxies or empty dict if file doesn't exist or is invalid
    """
    if not os.path.exists(PROXY_FILE):
        logger.debug(f"Proxy file {PROXY_FILE} not found")
        return {}
    
    try:
        with open(PROXY_FILE, 'r', encoding='utf-8') as file:
            proxies = json.load(file)
            logger.debug(f"Loaded {len(proxies)} proxies from file")
            return proxies
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {PROXY_FILE}: {e}")
        return {}
    except IOError as e:
        logger.error(f"Error reading {PROXY_FILE}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading proxies: {e}", exc_info=True)
        return {}


@app.route('/')
def index():
    """
    Render the main page with proxy information.
    
    Returns:
        Rendered HTML template with proxy data
    """
    try:
        proxies = load_proxies()
        # Pass configurable URLs to template
        template_vars = {
            'proxies': proxies,
            'proxy_channel_url': proxy_channel_url or 'https://t.me/Orv_Proxy',
            'config_channel_url': config_channel_url or 'https://t.me/Orv_Vpn',
            'bot_url': bot_url or 'https://t.me/OrBSup_bot',
            'support_url': support_url or 'https://t.me/Orv_Sup'
        }
        return render_template('index.html', **template_vars)
    except Exception as e:
        logger.error(f"Error rendering index page: {e}", exc_info=True)
        # Return empty proxies on error with default URLs
        template_vars = {
            'proxies': {},
            'proxy_channel_url': proxy_channel_url or 'https://t.me/Orv_Proxy',
            'config_channel_url': config_channel_url or 'https://t.me/Orv_Vpn',
            'bot_url': bot_url or 'https://t.me/OrBSup_bot',
            'support_url': support_url or 'https://t.me/Orv_Sup'
        }
        return render_template('index.html', **template_vars)


@app.route('/health')
def health():
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating service status
    """
    return {'status': 'ok', 'service': 'Orv Telegram Proxy'}


if __name__ == '__main__':
    # Only run directly if not being imported
    app.run(host='0.0.0.0', port=5000, debug=False)
