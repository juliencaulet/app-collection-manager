"""
Movie model for the application.
"""

from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class Movie(BaseDBModel):
    """
    Movie model representing a movie in the system.
    """
    title: str = Field(description="Title of the movie")
    director: str = Field(description="Director of the movie")
    year: int = Field(description="Release year")
    imdb_id: Optional[str] = Field(default=None, description="IMDb ID")
    genre: List[str] = Field(default_factory=list, description="List of genres")
    status: str = Field(default="owned", description="Current status of the movie")
    notes: Optional[str] = Field(default=None, description="Additional notes") 