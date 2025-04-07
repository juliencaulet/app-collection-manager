from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import sys
import logging
from pathlib import Path
from core.constants import (
    COLORS,
    EnvironmentType,
    LOG_LEVELS,
    DEFAULT_ENVIRONMENT,
    DEFAULT_ENV_FILE,
    DEFAULT_APP_NAME,
    DEFAULT_MONGODB_URL,
    DEFAULT_MONGODB_DB_NAME,
    DEFAULT_API_V1_STR,
    DEFAULT_LOG_LEVEL
)

class AlignedFormatter(logging.Formatter):
    """Custom formatter that aligns log messages based on level name length"""
    
    def format(self, record):
        # Get color for this level
        color = COLORS.get(record.levelname, COLORS['RESET'])
        # Format the level name and colon with color
        levelname = record.levelname
        colored_level = f"{color}{levelname}{COLORS['RESET']}:"
        # Calculate padding after the colon
        padding = 9 - len(levelname)  # DEBUG is 5 chars, so we need 4 spaces
        return f"{colored_level}{' ' * padding}{record.getMessage()}"

class FileFormatter(logging.Formatter):
    """Formatter for file logging"""
    
    def __init__(self):
        super().__init__('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    
    def format(self, record):
        return super().format(record)

def setup_logging(environment: EnvironmentType, log_level: str):
    """Setup logging configuration with both console and file handlers"""
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(AlignedFormatter())
    
    # Set up file handler
    log_file = logs_dir / f"{environment.value}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(FileFormatter())
    
    # Get numeric log level
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Configure uvicorn logger
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(numeric_level)
    uvicorn_logger.addHandler(console_handler)
    uvicorn_logger.addHandler(file_handler)
    
    # Configure uvicorn access logger
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.setLevel(numeric_level)
    uvicorn_access_logger.addHandler(console_handler)
    uvicorn_access_logger.addHandler(file_handler)
    
    # Get module-specific logger
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level {log_level}")
    logger.info(f"Log file: {log_file}")

# Get module-specific logger
logger = logging.getLogger(__name__)

def get_environment() -> EnvironmentType:
    """Get the current environment from environment variable or default to development"""
    env = os.getenv("ACM_ENVIRONMENT", DEFAULT_ENVIRONMENT).lower()
    try:
        environment = EnvironmentType(env)
        # Set the environment file based on the environment
        env_file = f".env.{environment.value}"
        if os.path.exists(env_file):
            # Get log level from environment
            log_level = os.getenv("ACM_LOG_LEVEL", DEFAULT_LOG_LEVEL)
            # Setup logging with environment-specific configuration
            setup_logging(environment, log_level)
        return environment
    except ValueError:
        logger.warning(f"Invalid environment '{env}', defaulting to {DEFAULT_ENVIRONMENT}")
        return EnvironmentType(DEFAULT_ENVIRONMENT)

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: EnvironmentType = get_environment()
    LOG_LEVEL: str = DEFAULT_LOG_LEVEL
    DEBUG: bool = True
    
    # Application settings
    APP_NAME: str = DEFAULT_APP_NAME
    
    # MongoDB settings
    MONGODB_URL: str = DEFAULT_MONGODB_URL
    MONGODB_DB_NAME: str = DEFAULT_MONGODB_DB_NAME
    
    # API settings
    API_V1_STR: str = DEFAULT_API_V1_STR
    
    class Config:
        env_file = os.getenv("ENV_FILE", DEFAULT_ENV_FILE)
        case_sensitive = True
        env_prefix = "ACM_"  # All environment variables should be prefixed with ACM_

# Get settings to load environment variables from file
settings = Settings()

# Reconfigure logging with settings from environment
log_level = LOG_LEVELS.get(settings.LOG_LEVEL.upper(), logging.INFO)
logging.getLogger().setLevel(log_level)
logger.debug("Logging reconfigured with level from settings")

@lru_cache()
def get_settings() -> Settings:
    logger.debug("Creating new Settings instance")
    logger.debug(f"Settings created with environment: {settings.ENVIRONMENT}")
    return settings 