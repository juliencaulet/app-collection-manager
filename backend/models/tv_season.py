"""
TV Season model for the application.

This module defines the TV Season model and its configuration for MongoDB storage.
The TV Season model represents a season of a television show in the system and includes fields for:
- Season identification (show_id, season_number)
- Production details (release_date, runtime)
- Classification (rating)
- Collection management (format, status)
- Media details (resolution, audio)
- Episode information (total_episodes)

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import Optional, List
from datetime import date
from pydantic import Field, constr
from .base import BaseDBModel, MongoDBConfig, PyObjectId

class TVSeason(BaseDBModel):
    """
    TV Season model representing a season of a television show in the system.
    
    This model includes fields for season identification, production details, and collection management.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        show_id (PyObjectId): ID of the TV show this season belongs to
        season_number (int): Number of the season (1-based)
        title (Optional[str]): Title of the season if different from show title
        release_date (Optional[date]): Release date of the season
        runtime (Optional[int]): Runtime per episode in minutes
        rating (Optional[str]): Season rating (e.g., TV-14, TV-MA)
        format (str): Format of the season (e.g., Blu-ray, DVD)
        resolution (Optional[str]): Video resolution (e.g., 1080p, 4K)
        audio (List[str]): Available audio tracks
        subtitles (List[str]): Available subtitle languages
        total_episodes (Optional[int]): Total number of episodes in this season
        collection_id (Optional[PyObjectId]): ID of the TV show collection this season belongs to
        status (str): Current status of the season (e.g., owned, wanted)
        notes (Optional[str]): Additional notes about the season
    """
    show_id: PyObjectId = Field(
        description="ID of the TV show this season belongs to"
    )
    season_number: int = Field(
        description="Number of the season (1-based)",
        ge=1
    )
    title: Optional[str] = Field(
        default=None,
        description="Title of the season if different from show title"
    )
    release_date: Optional[date] = Field(
        default=None,
        description="Release date of the season"
    )
    runtime: Optional[int] = Field(
        default=None,
        description="Runtime per episode in minutes",
        ge=1
    )
    rating: Optional[str] = Field(
        default=None,
        description="Season rating (e.g., TV-14, TV-MA)"
    )
    format: str = Field(
        description="Format of the season (e.g., Blu-ray, DVD)"
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
    total_episodes: Optional[int] = Field(
        default=None,
        description="Total number of episodes in this season",
        ge=1
    )
    collection_id: Optional[PyObjectId] = Field(
        default=None,
        description="ID of the TV show collection this season belongs to"
    )
    status: str = Field(
        default="owned",
        description="Current status of the season (e.g., owned, wanted)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the season"
    )

    class Config(MongoDBConfig):
        """
        Configuration for the TV Season model.
        
        This class defines the MongoDB collection name and indexes for the TV Season model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "tv_seasons"
        indexes = [
            {"key": {"show_id": 1}},
            {"key": {"season_number": 1}},
            {"key": {"release_date": 1}},
            {"key": {"collection_id": 1}},
            {"key": {"status": 1}},
            {"key": {"created_at": 1}},
            {"key": {"updated_at": 1}},
            {"key": {"show_id": 1, "season_number": 1}, "unique": True}  # Ensure unique season numbers per show
        ] 