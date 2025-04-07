"""
Database initialization for the Collection Manager application.

This module handles the creation and configuration of MongoDB collections and indexes.
"""

import logging
from typing import Dict, List, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

# Get module-specific logger
logger = logging.getLogger(__name__)

async def get_models() -> List[Any]:
    """
    Get all model classes.
    
    Returns:
        List[Any]: List of model classes
    """
    # Import models here to avoid circular imports
    from models.user import User
    from models.book import Book
    from models.book_series import BookSeries
    from models.movie import Movie
    from models.movie_collection import MovieCollection
    from models.tv_show import TVShow
    from models.tv_season import TVSeason

    return [
        User,
        Book,
        BookSeries,
        Movie,
        MovieCollection,
        TVShow,
        TVSeason
    ]

async def initialize_database(db: AsyncIOMotorDatabase) -> None:
    """
    Initialize the database with collections and indexes.
    
    Args:
        db: MongoDB database instance
    """
    try:
        models = await get_models()
        
        for model in models:
            # Create collection if it doesn't exist
            collection_name = model.Config.collection_name
            if collection_name not in await db.list_collection_names():
                await db.create_collection(collection_name)
                logger.info(f"Created collection {collection_name}")
            
            # Ensure indexes using the model's ensure_indexes method
            await model.ensure_indexes(db)
        
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise 