"""
Main FastAPI application entry point.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.environment import get_debug, get_cors_origins, get_environment, logger, get_configuration, get_port
from core.database import get_database
from api.routes import users, books, book_series, movies, movie_collections

# Get the port from environment
port = get_port()

app = FastAPI(
    title=f"App Collection Manager API ({get_environment().title()})",
    description="API for managing book and movie collections",
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

# Include routers
app.include_router(users.router)
app.include_router(books.router)
app.include_router(movies.router)
app.include_router(book_series.router)
app.include_router(movie_collections.router)

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