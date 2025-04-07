"""
Music Album model for the application.

This module defines the Music Album model and its configuration for MongoDB storage.
The Music Album model represents a music album in the system and includes fields for:
- Album identification (title, year, artist)
- Production details (label, format)
- Classification (genre, rating)
- Collection management (status, notes)
- Album details (tracks, duration)

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import Optional, List
from datetime import date
from pydantic import Field, constr
from .base import BaseDBModel, MongoDBConfig

class MusicAlbum(BaseDBModel):
    """
    Music Album model representing a music album in the system.
    
    This model includes fields for album identification, production details, and collection management.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        title (str): Title of the album (1-200 characters)
        original_title (Optional[str]): Original title in the album's language
        year (int): Release year of the album
        artist (str): Artist of the album (1-100 characters)
        label (Optional[str]): Record label
        format (str): Format of the album (e.g., CD, vinyl, digital)
        genre (List[str]): List of genres the album belongs to
        rating (Optional[str]): Album rating (e.g., E, E10+, T)
        tracks (Optional[int]): Number of tracks
        duration (Optional[int]): Total duration in minutes
        collection_id (Optional[PyObjectId]): ID of the music collection this album belongs to
        status (str): Current status of the album (e.g., owned, wanted)
        notes (Optional[str]): Additional notes about the album
    """
    title: constr(min_length=1, max_length=200) = Field(
        description="Title of the album"
    )
    original_title: Optional[str] = Field(
        default=None,
        description="Original title in the album's language"
    )
    year: int = Field(
        description="Release year of the album",
        ge=1877  # First music recording
    )
    artist: constr(min_length=1, max_length=100) = Field(
        description="Artist of the album"
    )
    label: Optional[str] = Field(
        default=None,
        description="Record label"
    )
    format: str = Field(
        description="Format of the album (e.g., CD, vinyl, digital)"
    )
    genre: List[str] = Field(
        default_factory=list,
        description="List of genres the album belongs to"
    )
    rating: Optional[str] = Field(
        default=None,
        description="Album rating (e.g., E, E10+, T)"
    )
    tracks: Optional[int] = Field(
        default=None,
        description="Number of tracks",
        ge=1
    )
    duration: Optional[int] = Field(
        default=None,
        description="Total duration in minutes",
        ge=1
    )
    collection_id: Optional[PyObjectId] = Field(
        default=None,
        description="ID of the music collection this album belongs to"
    )
    status: str = Field(
        default="owned",
        description="Current status of the album (e.g., owned, wanted)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the album"
    )

    class Config(MongoDBConfig):
        """
        Configuration for the Music Album model.
        
        This class defines the MongoDB collection name and indexes for the Music Album model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "music_albums"
        indexes = [
            {"key": {"title": 1}},
            {"key": {"year": 1}},
            {"key": {"artist": 1}},
            {"key": {"genre": 1}},
            {"key": {"collection_id": 1}},
            {"key": {"status": 1}},
            {"key": {"created_at": 1}},
            {"key": {"updated_at": 1}}
        ] 