from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class Movie(BaseDBModel):
    title: str = Field(..., min_length=1, max_length=200)
    original_title: Optional[str] = Field(None, max_length=200)
    release_year: Optional[int] = Field(None, ge=1888, le=2100)  # First movie was in 1888
    director: Optional[str] = Field(None, max_length=100)
    runtime: Optional[int] = Field(None, ge=1)  # in minutes
    description: Optional[str] = Field(None, max_length=2000)
    genres: List[str] = Field(default_factory=list)
    imdb_id: Optional[str] = Field(None, min_length=9, max_length=9)  # tt + 7 digits
    collection_id: Optional[str] = Field(None)
    poster_url: Optional[str] = Field(None)
    owner_id: str = Field(...)
    
    class Config:
        collection_name = "acm_movies"
        indexes = [
            {"key": [("title", 1), ("release_year", 1)], "unique": True},
            {"key": [("imdb_id", 1)], "unique": True, "sparse": True},
            {"key": [("owner_id", 1)]},
            {"key": [("collection_id", 1)]}
        ] 