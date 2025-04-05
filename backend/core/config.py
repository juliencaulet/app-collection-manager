from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import sys
import logging
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

# Setup initial logging with default configuration
handler = logging.StreamHandler()
handler.setFormatter(AlignedFormatter())
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)

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
            os.environ["ENV_FILE"] = env_file
            logger.info(f"Using environment file: {env_file}")
        return environment
    except ValueError:
        valid_envs = [e.value for e in EnvironmentType]
        logger.error(f"Invalid environment '{env}'")
        logger.info(f"Valid environments are: {', '.join(valid_envs)}")
        sys.exit(1)

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