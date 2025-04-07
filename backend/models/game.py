"""
Game model for the application.

This module defines the Game model and its configuration for MongoDB storage.
The Game model represents a video game in the system and includes fields for:
- Game identification (title, year, developer)
- Production details (publisher, platform)
- Classification (genre, rating)
- Collection management (format, status)
- Game details (players, completion time)

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import Optional, List
from datetime import date
from pydantic import Field, constr
from .base import BaseDBModel, MongoDBConfig

class Game(BaseDBModel):
    """
    Game model representing a video game in the system.
    
    This model includes fields for game identification, production details, and collection management.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        title (str): Title of the game (1-200 characters)
        original_title (Optional[str]): Original title in the game's language
        year (int): Release year of the game
        developer (str): Developer of the game (1-100 characters)
        publisher (Optional[str]): Publisher of the game
        platform (str): Platform the game is for (e.g., PC, PS5, Xbox)
        genre (List[str]): List of genres the game belongs to
        rating (Optional[str]): Game rating (e.g., E, T, M)
        format (str): Format of the game (e.g., physical, digital)
        players (Optional[int]): Number of players supported
        completion_time (Optional[int]): Average completion time in hours
        collection_id (Optional[PyObjectId]): ID of the game collection this game belongs to
        status (str): Current status of the game (e.g., owned, wanted)
        notes (Optional[str]): Additional notes about the game
    """
    title: constr(min_length=1, max_length=200) = Field(
        description="Title of the game"
    )
    original_title: Optional[str] = Field(
        default=None,
        description="Original title in the game's language"
    )
    year: int = Field(
        description="Release year of the game",
        ge=1958  # First video game ever made
    )
    developer: constr(min_length=1, max_length=100) = Field(
        description="Developer of the game"
    )
    publisher: Optional[str] = Field(
        default=None,
        description="Publisher of the game"
    )
    platform: str = Field(
        description="Platform the game is for (e.g., PC, PS5, Xbox)"
    )
    genre: List[str] = Field(
        default_factory=list,
        description="List of genres the game belongs to"
    )
    rating: Optional[str] = Field(
        default=None,
        description="Game rating (e.g., E, T, M)"
    )
    format: str = Field(
        description="Format of the game (e.g., physical, digital)"
    )
    players: Optional[int] = Field(
        default=None,
        description="Number of players supported",
        ge=1
    )
    completion_time: Optional[int] = Field(
        default=None,
        description="Average completion time in hours",
        ge=1
    )
    collection_id: Optional[PyObjectId] = Field(
        default=None,
        description="ID of the game collection this game belongs to"
    )
    status: str = Field(
        default="owned",
        description="Current status of the game (e.g., owned, wanted)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the game"
    )

    class Config(MongoDBConfig):
        """
        Configuration for the Game model.
        
        This class defines the MongoDB collection name and indexes for the Game model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "games"
        indexes = [
            {"key": {"title": 1}},
            {"key": {"year": 1}},
            {"key": {"developer": 1}},
            {"key": {"platform": 1}},
            {"key": {"genre": 1}},
            {"key": {"collection_id": 1}},
            {"key": {"status": 1}},
            {"key": {"created_at": 1}},
            {"key": {"updated_at": 1}}
        ] 