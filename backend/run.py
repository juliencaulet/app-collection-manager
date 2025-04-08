"""
Script to run the FastAPI application with the correct port from environment.
"""

import uvicorn
from config.environment import logger, get_environment, get_port, get_log_file
import logging

def log_startup(port: int):
    """Log startup information."""
    env = get_environment()
    logger.info("- RUN SERVER ------------------------------------------------")
    logger.info(f"Starting {env} environment")
    logger.info(f"Application configured to run on port: {port}")

if __name__ == "__main__":
    # Get port from app state
    port = get_port()
    log_startup(port)
    
    # Get the log file path
    log_file = get_log_file()
    
    # Create a custom logging config for Uvicorn
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Configure file handler for Uvicorn
    file_handler = logging.FileHandler(log_file)
    # file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    # Add file handler to Uvicorn's logger
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.addHandler(file_handler)
    
    # Create the config first
    config = uvicorn.Config(
        "main:app", 
        host="0.0.0.0", 
        port=port,
        reload=True,
        log_config=log_config,
        log_level="debug"
    )
    
    # Run the server
    server = uvicorn.Server(config)
    server.run() 
