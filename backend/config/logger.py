import logging
import sys
from datetime import datetime
from pathlib import Path
import os

# ANSI color codes
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"

class UvicornFormatter(logging.Formatter):
    """Custom formatter that matches Uvicorn's style."""
    
    def format(self, record):
        
        # Format the log level with appropriate color and style
        levelname = record.levelname
        if levelname == "INFO":
            levelname = f"{GREEN}{levelname}{RESET}:"
        elif levelname == "WARNING":
            levelname = f"{YELLOW}{levelname}{RESET}:"
        elif levelname == "ERROR":
            levelname = f"{RED}{levelname}{RESET}:"
        elif levelname == "DEBUG":
            levelname = f"{BLUE}{levelname}{RESET}:"
        
        # Format the message with appropriate style
        message = record.getMessage()
        if record.levelname == "INFO":
            message = f"{BOLD}{message}{RESET}"
        elif record.levelname == "ERROR":
            message = f"{RED}{message}{RESET}"
        elif record.levelname == "WARNING":
            message = f"{YELLOW}{message}{RESET}"
        
        return f"{levelname:18} {message}"

class PlainFormatter(logging.Formatter):
    """Formatter that removes ANSI color codes."""
    def format(self, record):
        # Get the current time
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the message without colors
        message = record.getMessage()
        # Remove ANSI color codes
        for code in [BLUE, GREEN, YELLOW, RED, BOLD, RESET]:
            message = message.replace(code, '')
        
        return f"{timestamp} | {record.levelname:8} | {message}"

def setup_logger(log_file: str = None, log_level: str = "INFO") -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    # Create console handler with Uvicorn formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(UvicornFormatter())
    logger.addHandler(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        # Ensure the logs directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a file stream that flushes immediately
        file_stream = open(log_file, 'a', encoding='utf-8')
        file_handler = logging.StreamHandler(file_stream)
        file_handler.setFormatter(PlainFormatter())
        logger.addHandler(file_handler)
    
    # Remove any existing handlers to avoid duplicate logs
    logger.propagate = False
    
    return logger

# Create a default logger instance
logger = setup_logger() 