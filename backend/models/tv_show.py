"""
TV Show model for the application.

This module defines the TV Show model and its configuration for MongoDB storage.
The TV Show model represents a television show in the system and includes fields for:
- Show identification (title, year, network)
- Production details (studio, runtime)
- Classification (genre, rating)
- Collection management (format, status)
- Media details (resolution, audio)
- Series information (seasons, episodes)

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import Optional, List
from datetime import date, datetime
from pydantic import Field, constr
from .base import BaseDBModel, MongoDBConfig
from .common import PyObjectId
from bson import ObjectId

class TVShow(BaseDBModel):
    """
    TV Show model representing a television series in the system.
    
    This model includes fields for show identification, production details, and collection management.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        title (str): Title of the TV show (1-200 characters)
        original_title (Optional[str]): Original title in the show's language
        year_started (int): Year the show started
        year_ended (Optional[int]): Year the show ended
        creator (str): Creator of the show (1-100 characters)
        studio (Optional[str]): Production studio
        runtime (Optional[int]): Runtime per episode in minutes
        genre (List[str]): List of genres the show belongs to
        rating (Optional[str]): Show rating (e.g., TV-MA, TV-14)
        format (str): Format of the show (e.g., Blu-ray, DVD)
        resolution (Optional[str]): Video resolution (e.g., 1080p, 4K)
        audio (List[str]): Available audio tracks
        subtitles (List[str]): Available subtitle languages
        collection_id (Optional[PyObjectId]): ID of the show collection this show belongs to
        status (str): Current status of the show (e.g., owned, wanted)
        notes (Optional[str]): Additional notes about the show
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: constr(min_length=1, max_length=200) = Field(
        description="Title of the TV show"
    )
    original_title: Optional[str] = Field(
        default=None,
        description="Original title in the show's language"
    )
    year_started: int = Field(
        description="Year the show started",
        ge=1928  # First TV show ever made
    )
    year_ended: Optional[int] = Field(
        default=None,
        description="Year the show ended",
        ge=1928
    )
    creator: constr(min_length=1, max_length=100) = Field(
        description="Creator of the show"
    )
    studio: Optional[str] = Field(
        default=None,
        description="Production studio"
    )
    runtime: Optional[int] = Field(
        default=None,
        description="Runtime per episode in minutes",
        ge=1
    )
    genre: List[str] = Field(
        default_factory=list,
        description="List of genres the show belongs to"
    )
    rating: Optional[str] = Field(
        default=None,
        description="Show rating (e.g., TV-MA, TV-14)"
    )
    format: str = Field(
        description="Format of the show (e.g., Blu-ray, DVD)"
    )
    resolution: Optional[str] = Field(
        default=None,
        description="Video resolution (e.g., 1080p, 4K)"
    )
    audio: List[str] = Field(
        default_factory=list,
        description="Available audio tracks"
    )
    subtitles: List[str] = Field(
        default_factory=list,
        description="Available subtitle languages"
    )
    collection_id: Optional[PyObjectId] = Field(
        default=None,
        description="ID of the show collection this show belongs to"
    )
    status: str = Field(
        default="owned",
        description="Current status of the show (e.g., owned, wanted)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the show"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config(MongoDBConfig):
        """
        Configuration for the TV Show model.
        
        This class defines the MongoDB collection name and indexes for the TV Show model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "tv_shows"
        indexes = [
            {"key": {"title": 1}},
            {"key": {"year": 1}},
            {"key": {"network": 1}},
            {"key": {"genre": 1}},
            {"key": {"collection_id": 1}},
            {"key": {"status": 1}},
            {"key": {"created_at": 1}},
            {"key": {"updated_at": 1}}
        ] 