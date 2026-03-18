import logging
import logging.handlers
import os
from pathlib import Path

def setup_logging():
    # Use absolute path relative to this file
    # this file is at backend/app/core/logging.py
    # we want backend/logs
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    log_dir = base_dir / "logs"
    
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a timed rotating file handler
    # Rotates at midnight, keeps 30 days of logs
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
    )
    file_handler.suffix = "%Y-%m-%d"
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
