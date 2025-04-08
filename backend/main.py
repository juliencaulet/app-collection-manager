"""
Main FastAPI application entry point.
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.environment import get_debug, get_cors_origins, get_environment, logger, get_configuration, get_port, get_api_prefix
from core.database import get_database
from api.v1.api import router as api_router
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"{get_environment()}.log")
handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger("uvicorn")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Get the port from environment
port = get_port()

app = FastAPI(
    title=f"App Collection Manager API ({get_environment().title()})",
    description="API for managing collections of books, movies, and TV shows",
    version="1.0.0",
    debug=get_debug()
)

# Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=get_cors_origins(),
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include API routes
app.include_router(api_router, prefix=get_api_prefix())

@app.get("/")
async def root():
    return {"message": "Welcome to App Collection Manager API"}

@app.get("/config")
async def config(): 
    return get_configuration()

@app.on_event("startup")
async def startup_event():
    """Perform startup tasks."""
    try:
        logger.info("- STARTUP --------------------------------------------------")
        # Test database connection
        db = get_database()
        # Use admin command to test connection
        await db.command('ping')
        logger.info("Database connection successful")
        
        # Get collections and database info
        collections = await db.list_collection_names()
        logger.info(f"Database: {db.name}")
        logger.info(f"Collections: {', '.join(collections)}")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Perform shutdown tasks."""
    try:
        logger.info("- SHUTDOWN --------------------------------------------------")
        db = get_database()
        db.client.close()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database connection: {str(e)}") 