"""
Database initialization for the Collection Manager application.

This module handles the creation and configuration of MongoDB collections and indexes.
"""

import logging
from typing import Dict, List, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

# Get module-specific logger
logger = logging.getLogger(__name__)

async def get_model_configs() -> Dict[str, Dict[str, Any]]:
    """
    Get configurations for all models.
    
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of model configurations
    """
    # Import models here to avoid circular imports
    from models.user import User
    from models.book import Book
    from models.book_series import BookSeries
    from models.movie import Movie
    from models.movie_collection import MovieCollection
    from models.tv_show import TVShow
    from models.tv_season import TVSeason

    return {
        "users": User.Config,
        "books": Book.Config,
        "book_series": BookSeries.Config,
        "movies": Movie.Config,
        "movie_collections": MovieCollection.Config,
        "tv_shows": TVShow.Config,
        "tv_seasons": TVSeason.Config
    }

async def create_indexes(db: AsyncIOMotorDatabase, collection_name: str, indexes: List[Dict[str, Any]]) -> None:
    """
    Create indexes for a collection.
    
    Args:
        db: MongoDB database instance
        collection_name: Name of the collection
        indexes: List of index configurations
    """
    try:
        collection = db[collection_name]
        for index in indexes:
            # Extract keys and options from the index configuration
            # Support both 'key' and 'keys' for backward compatibility
            keys = index.get('keys', index.get('key', {}))
            options = {k: v for k, v in index.items() if k not in ['keys', 'key']}
            
            if not keys:
                logger.warning(f"Skipping index creation for {collection_name}: no keys specified")
                continue
                
            await collection.create_index(keys, **options)
            logger.info(f"Created index {keys} for collection {collection_name}")
    except Exception as e:
        logger.error(f"Failed to create indexes for collection {collection_name}: {str(e)}")
        raise

async def initialize_database(db: AsyncIOMotorDatabase) -> None:
    """
    Initialize the database with collections and indexes.
    
    Args:
        db: MongoDB database instance
    """
    try:
        model_configs = await get_model_configs()
        
        for collection_name, config in model_configs.items():
            # Create collection if it doesn't exist
            if collection_name not in await db.list_collection_names():
                await db.create_collection(collection_name)
                logger.info(f"Created collection {collection_name}")
            
            # Create indexes
            if hasattr(config, 'indexes'):
                await create_indexes(db, collection_name, config.indexes)
        
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise 