from enum import Enum
import logging

# ANSI color codes for terminal output
COLORS = {
    'DEBUG': '\033[36m',    # Cyan
    'INFO': '\033[32m',     # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',    # Red
    'CRITICAL': '\033[35m', # Magenta
    'RESET': '\033[0m'      # Reset
}

# Environment types
class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

# Log levels
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Default values
DEFAULT_ENVIRONMENT = "development"
DEFAULT_ENV_FILE = ".env"
DEFAULT_APP_NAME = "App Collection Manager"
DEFAULT_MONGODB_URL = "mongodb://localhost:27017"
DEFAULT_MONGODB_DB_NAME = "acm_db"
DEFAULT_API_V1_STR = "/api/v1"
DEFAULT_LOG_LEVEL = "INFO" 