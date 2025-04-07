"""
Movie model for the application.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    director: str
    year: Optional[int] = None
    description: Optional[str] = None
    duration: Optional[int] = None  # in minutes
    language: Optional[str] = None
    poster_image: Optional[str] = None
    genre: Optional[str] = None
    status: str = "unwatched"  # unwatched, watching, watched
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    collection_id: Optional[str] = None
    collection_order: Optional[int] = None
    studio: Optional[str] = None
    cast: List[str] = []
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "acm_movies"
        json_schema_extra = {
            "example": {
                "title": "The Lord of the Rings: The Fellowship of the Ring",
                "director": "Peter Jackson",
                "year": 2001,
                "description": "A meek Hobbit from the Shire and eight companions...",
                "duration": 178,
                "language": "English",
                "genre": "Fantasy",
                "status": "unwatched",
                "studio": "New Line Cinema",
                "cast": ["Elijah Wood", "Ian McKellen"],
                "tags": ["fantasy", "adventure"]
            }
        }
        populate_by_name = True
        indexes = [
            {"key": [("title", 1)]},
            {"key": [("director", 1)]},
            {"key": [("year", 1)]},
            {"key": [("genre", 1)]},
            {"key": [("status", 1)]},
            {"key": [("collection_id", 1)]},
            {"key": [("studio", 1)]},
            {"key": [("tags", 1)]}
        ] 