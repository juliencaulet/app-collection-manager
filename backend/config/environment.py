import os
from dotenv import load_dotenv
from pathlib import Path
import logging
import sys
from datetime import datetime

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
        # Get the current time
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the log level with appropriate color and style
        levelname = record.levelname
        if levelname == "INFO":
            levelname = f"{GREEN}ℹ {levelname}{RESET}"
        elif levelname == "WARNING":
            levelname = f"{YELLOW}⚠ {levelname}{RESET}"
        elif levelname == "ERROR":
            levelname = f"{RED}✖ {levelname}{RESET}"
        elif levelname == "DEBUG":
            levelname = f"{BLUE}⚙ {levelname}{RESET}"
        
        # Format the message with appropriate style
        message = record.getMessage()
        if record.levelname == "INFO":
            message = f"{BOLD}{message}{RESET}"
        elif record.levelname == "ERROR":
            message = f"{RED}{message}{RESET}"
        elif record.levelname == "WARNING":
            message = f"{YELLOW}{message}{RESET}"
        
        # Add a separator line for better readability
        separator = f"{BLUE}─{RESET}" * 80
        
        return f"\n{separator}\n{timestamp} | {levelname} | {message}\n{separator}"

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
        
        return f"{timestamp} | {record.levelname} | {message}"

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler with Uvicorn formatter
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(UvicornFormatter())
logger.addHandler(console_handler)

# Remove any existing handlers to avoid duplicate logs
logger.propagate = False

def get_environment() -> str:
    """Get the current environment."""
    return os.getenv("ACM_ENVIRONMENT", "development")

def is_development() -> bool:
    """Check if the current environment is development."""
    return get_environment() == "development"

def is_production() -> bool:
    """Check if the current environment is production."""
    return get_environment() == "production"

def get_log_file() -> str:
    """Get the log file path based on the environment."""
    env = get_environment()
    return os.getenv("LOG_FILE", f"logs/{env}.log")

def get_mongodb_url() -> str:
    """Get the MongoDB URL based on the environment."""
    if is_production():
        return os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
    return os.getenv("MONGODB_URL", "mongodb://localhost:27017")

def get_mongodb_db_name() -> str:
    """Get the MongoDB database name based on the environment."""
    env = get_environment()
    return os.getenv("MONGODB_DB_NAME", f"acm_{env}")

def get_cors_origins() -> list[str]:
    """Get the CORS origins based on the environment."""
    return eval(os.getenv("CORS_ORIGINS", "[]"))

def get_debug() -> bool:
    """Get the debug setting based on the environment."""
    # If ACM_ENVIRONMENT is not set, default to True
    if not os.getenv("ACM_ENVIRONMENT"):
        return True
    return os.getenv("DEBUG", "False").lower() == "true"

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
    
    logger.info("Application Configuration:")
    for key, value in config.items():
        logger.info(f"{BLUE}{key}{RESET}: {value}")

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