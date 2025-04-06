"""
Database connection management for the Collection Manager application.

This module handles MongoDB connection and provides a database instance.
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient

# Get module-specific logger
logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        """Connect to MongoDB."""
        try:
            from core.config import get_settings
            settings = get_settings()
            
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            self.db = self.client[settings.MONGODB_DB_NAME]
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    async def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")

    def get_db(self):
        """Get database instance."""
        return self.db

# Create a single instance
database = Database() 