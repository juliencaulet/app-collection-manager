from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from core.config import get_settings, EnvironmentType
from core.errors import CollectionManagerError

# Get module-specific logger
logger = logging.getLogger(__name__)

# Get settings
logger.debug("Loading settings in main.py")
settings = get_settings()
logger.debug(f"Settings loaded with environment: {settings.ENVIRONMENT}")

# Log startup information
logger.info(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} environment")
if settings.DEBUG:
    logger.warning("Debug mode is enabled")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="API for managing collections of books and video content",
    version="0.1.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Settings endpoint
@app.get("/settings")
async def get_app_settings():
    """Return current application settings (excluding sensitive information)"""
    logger.debug("Accessing settings endpoint")
    settings_response = {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "api_version": settings.API_V1_STR,
        "mongodb_db_name": settings.MONGODB_DB_NAME,
        "mongodb_url": settings.MONGODB_URL  # Always include the URL for now
    }
    logger.debug(f"Settings response: {settings_response}")
    return settings_response

# Error handler
@app.exception_handler(CollectionManagerError)
async def collection_manager_error_handler(request, exc: CollectionManagerError):
    return {"detail": exc.detail}, exc.status_code 