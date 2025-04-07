"""
Base models and configurations for MongoDB collections.

This module provides the base classes and utilities for all data models in the application.
It includes:
- PyObjectId: Custom type for MongoDB ObjectId handling
- MongoDBConfig: Configuration class for MongoDB collections
- BaseDBModel: Base model class for all database entities

The module ensures consistent handling of MongoDB ObjectIds, timestamps, and audit fields
across all models in the application.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, ClassVar
from pydantic import BaseModel, Field, GetJsonSchemaHandler, ConfigDict
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson import ObjectId
import logging

# Configure logging
logger = logging.getLogger(__name__)

class PyObjectId(str):
    """
    Custom type for MongoDB ObjectId handling.
    
    This class provides validation and serialization for MongoDB ObjectIds in Pydantic models.
    It ensures that ObjectIds are properly validated and serialized to strings in JSON responses.
    
    Attributes:
        None (inherits from str)
        
    Methods:
        __get_pydantic_core_schema__: Returns the core schema for Pydantic validation
        __get_pydantic_json_schema__: Returns the JSON schema for serialization
    """
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetJsonSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        Returns the core schema for Pydantic validation.
        
        Args:
            _source_type: The source type being validated
            _handler: The schema handler
            
        Returns:
            core_schema.CoreSchema: The core schema for validation
        """
        def validate(value: str) -> str:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return str(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _schema_generator: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        """
        Returns the JSON schema for serialization.
        
        Args:
            _schema_generator: The schema generator
            
        Returns:
            JsonSchemaValue: The JSON schema
        """
        return {"type": "string"}

class MongoDBConfig:
    """
    Base configuration for MongoDB models.
    
    This class provides default configuration for MongoDB collections,
    including collection names and index definitions.
    """
    collection_name: str = ""
    indexes: List[Dict[str, Any]] = []
    json_encoders: Dict[type, Any] = { 
        ObjectId: str, 
        datetime: lambda dt: dt.isoformat()
    }

class BaseDBModel(BaseModel):
    """
    Base model for all database models.
    
    This class provides common functionality and configuration for all database models.
    It includes methods for database operations and configuration for MongoDB.
    """
    id: Optional[str] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config(MongoDBConfig):
        """
        Configuration for the base model.
        
        This class defines the default MongoDB configuration for all models.
        """
        pass

    @classmethod
    async def ensure_indexes(cls, db):
        """
        Ensure all indexes are properly created for the collection.
        This method first drops all existing indexes and then creates new ones
        to avoid conflicts with existing indexes.
        
        Args:
            db: MongoDB database instance
            
        Raises:
            Exception: If there's an error creating or dropping indexes
        """
        try:
            collection = db[cls.Config.collection_name]
            logger.info(f"Ensuring indexes for collection: {cls.Config.collection_name}")
            
            # Get existing indexes
            existing_indexes = []
            async for index in collection.list_indexes():
                existing_indexes.append(index)
            logger.debug(f"Existing indexes: {existing_indexes}")
            
            # Drop all existing indexes except _id
            for index in existing_indexes:
                if index["name"] != "_id_":
                    try:
                        await collection.drop_index(index["name"])
                        logger.debug(f"Dropped index: {index['name']}")
                    except Exception as e:
                        logger.warning(f"Failed to drop index {index['name']}: {str(e)}")
            
            # Create new indexes
            for index in cls.Config.indexes:
                try:
                    # Extract keys and options from the index configuration
                    keys = index.get('key', {})
                    options = {k: v for k, v in index.items() if k not in ['key', 'keys']}
                    await collection.create_index(keys, **options)
                    logger.debug(f"Created index: {options.get('name', 'unnamed')}")
                except Exception as e:
                    logger.error(f"Failed to create index {options.get('name', 'unnamed')}: {str(e)}")
                    raise
            
            logger.info(f"Successfully ensured indexes for collection: {cls.Config.collection_name}")
            
        except Exception as e:
            logger.error(f"Error ensuring indexes for {cls.Config.collection_name}: {str(e)}")
            raise 