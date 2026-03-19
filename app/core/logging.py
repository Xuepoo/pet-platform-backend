"""Logging configuration for the application.

This module sets up logging with timed rotating file handlers
and console output for the Pet Platform application.
"""

import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging() -> None:
    """Configure application logging with file rotation and console output.
    
    Sets up a timed rotating file handler that rotates at midnight and keeps
    30 days of logs. Also configures console output for development.
    
    The log files are stored in the `logs/` directory relative to the
    backend root directory.
    
    Returns:
        None
    """
    base_dir = Path(__file__).resolve().parent.parent.parent
    log_dir = base_dir / "logs"
    
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
    )
    file_handler.suffix = "%Y-%m-%d"
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
