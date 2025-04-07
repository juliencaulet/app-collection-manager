"""
Movie model for the application.

This module defines the Movie model and its configuration for MongoDB storage.
The Movie model represents a movie in the system and includes fields for:
- Movie identification (title, year, director)
- Production details (studio, runtime)
- Classification (genre, rating)
- Collection management (format, status)
- Media details (resolution, audio)

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import Optional, List, Any
from datetime import date, datetime
from pydantic import Field, constr, GetJsonSchemaHandler, GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from .base import BaseDBModel, MongoDBConfig
from .common import PyObjectId
from bson import ObjectId

class Movie(BaseDBModel):
    """
    Movie model representing a movie in the system.
    
    This model includes fields for movie identification, production details, and collection management.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        title (str): Title of the movie (1-200 characters)
        original_title (Optional[str]): Original title in the movie's language
        year (int): Release year of the movie
        director (str): Director of the movie (1-100 characters)
        studio (Optional[str]): Production studio
        runtime (Optional[int]): Runtime in minutes
        genre (List[str]): List of genres the movie belongs to
        rating (Optional[str]): Movie rating (e.g., PG, R)
        format (str): Format of the movie (e.g., Blu-ray, DVD)
        resolution (Optional[str]): Video resolution (e.g., 1080p, 4K)
        audio (List[str]): Available audio tracks
        subtitles (List[str]): Available subtitle languages
        collection_id (Optional[PyObjectId]): ID of the movie collection this movie belongs to
        status (str): Current status of the movie (e.g., owned, wanted)
        notes (Optional[str]): Additional notes about the movie
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: constr(min_length=1, max_length=200) = Field(
        description="Title of the movie"
    )
    original_title: Optional[str] = Field(
        default=None,
        description="Original title in the movie's language"
    )
    year: int = Field(
        description="Release year of the movie",
        ge=1888  # First movie ever made
    )
    director: constr(min_length=1, max_length=100) = Field(
        description="Director of the movie"
    )
    studio: Optional[str] = Field(
        default=None,
        description="Production studio"
    )
    runtime: Optional[int] = Field(
        default=None,
        description="Runtime in minutes",
        ge=1
    )
    genre: List[str] = Field(
        default_factory=list,
        description="List of genres the movie belongs to"
    )
    rating: Optional[str] = Field(
        default=None,
        description="Movie rating (e.g., PG, R)"
    )
    format: str = Field(
        description="Format of the movie (e.g., Blu-ray, DVD)"
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
        description="ID of the movie collection this movie belongs to"
    )
    status: str = Field(
        default="owned",
        description="Current status of the movie (e.g., owned, wanted)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the movie"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config(MongoDBConfig):
        """
        Configuration for the Movie model.
        
        This class defines the MongoDB collection name and indexes for the Movie model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "movies"
        indexes = [
            {"key": {"title": 1}},
            {"key": {"year": 1}},
            {"key": {"director": 1}},
            {"key": {"genre": 1}},
            {"key": {"collection_id": 1}},
            {"key": {"status": 1}},
            {"key": {"created_at": 1}},
            {"key": {"updated_at": 1}}
        ]
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
        schema_extra = {
            "example": {
                "title": "Inception",
                "year": 2010,
                "director": "Christopher Nolan",
                "genre": ["Action", "Sci-Fi", "Thriller"],
                "rating": 8.8,
                "collection_id": "507f1f77bcf86cd799439011"
            }
        } 