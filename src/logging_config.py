"""
Centralized logging configuration for the application.
This ensures consistent logging setup across all modules.
"""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure logging for the entire application.
    
    Args:
        level: Logging level (default: INFO)
    """
    # Only configure if not already configured (avoid duplicate handlers)
    if logging.root.handlers:
        return
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout,
        force=True  # Override any existing configuration
    )

