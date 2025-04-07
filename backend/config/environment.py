import os
from dotenv import load_dotenv
from pathlib import Path
from config.logger import logger, PlainFormatter
import sys
import logging

def get_environment() -> str:
    """Get the current environment."""
    return os.getenv("ACM_ENVIRONMENT", "development")

def get_debug() -> bool:
    """Get the debug mode setting."""
    return os.getenv("DEBUG", "False").lower() == "true"

def get_mongodb_url() -> str:
    """Get the MongoDB URL."""
    return os.getenv("MONGODB_URL", "mongodb://localhost:27017")

def get_mongodb_db_name() -> str:
    """Get the MongoDB database name."""
    return os.getenv("MONGODB_DB_NAME", "acm_db")

def get_cors_origins() -> list:
    """Get the CORS origins."""
    origins = os.getenv("CORS_ORIGINS", "[]")
    # Remove quotes and brackets, then split by comma
    return [origin.strip() for origin in origins.strip("[]").split(",") if origin.strip()]

def get_log_file() -> str:
    """Get the log file path."""
    return os.getenv("LOG_FILE", "logs/app.log")

def display_configuration():
    """Display the current configuration in the logs."""
    config = {
        "Environment": get_environment(),
        "Debug Mode": get_debug(),
        "MongoDB URL": get_mongodb_url(),
        "MongoDB Database": get_mongodb_db_name(),
        "CORS Origins": get_cors_origins(),
        "Log File": get_log_file(),
        "Log Level": os.getenv("LOG_LEVEL", "INFO"),
        "API Version": os.getenv("API_V1_STR", "/api/v1"),
        "Token Expiration (minutes)": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    }
    
    # System information
    system_info = {
        "Python Version": sys.version,
        "Platform": sys.platform,
        "Working Directory": os.getcwd(),
        "Environment Files": {
            "Base": str(Path(__file__).parent / ".env"),
            "Current": str(Path(__file__).parent / f".env.{get_environment()}")
        }
    }
    
    logger.info("Application Configuration:")
    for key, value in config.items():
        logger.info(f"{key}: {value}")
    
    logger.debug("System Information:")
    for key, value in system_info.items():
        logger.debug(f"{key}: {value}")
    
    # Log file information
    log_file = get_log_file()
    log_path = Path(log_file)
    logger.debug(f"Log file path: {log_path.absolute()}")
    logger.debug(f"Log file exists: {log_path.exists()}")
    logger.debug(f"Log file size: {log_path.stat().st_size if log_path.exists() else 0} bytes")

def load_environment():
    """Load the appropriate environment file based on ACM_ENVIRONMENT."""
    # Default to development if not set
    env = os.getenv("ACM_ENVIRONMENT", "development")
    env_file = f".env.{env}"
    
    # First try to load the environment-specific file
    env_path = Path(__file__).parent / env_file
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Loaded environment configuration from {env_file}")
    else:
        logger.warning(f"Environment file {env_file} not found, using default configuration")
    
    # Then load the base .env file as fallback
    base_env_path = Path(__file__).parent / ".env"
    load_dotenv(base_env_path)
    
    # Ensure ACM_ENVIRONMENT is set to development if not defined
    if not os.getenv("ACM_ENVIRONMENT"):
        os.environ["ACM_ENVIRONMENT"] = "development"
        os.environ["DEBUG"] = "True"
    
    # Set the log level from environment
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logger.setLevel(log_level)
    logger.info(f"Log level set to {log_level}")
    
    # Configure file handler after environment is loaded
    log_file = get_log_file()
    # Ensure the logs directory exists
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a file stream that flushes immediately
    file_stream = open(log_file, 'a', encoding='utf-8')
    file_handler = logging.StreamHandler(file_stream)
    file_handler.setFormatter(PlainFormatter())
    logger.addHandler(file_handler)
    
    # Display configuration after loading
    display_configuration()

# Load environment variables
load_environment() 