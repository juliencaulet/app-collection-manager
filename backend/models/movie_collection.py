from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class MovieCollection(BaseDBModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    genres: List[str] = Field(default_factory=list)
    total_movies: int = Field(default=0, ge=0)
    poster_url: Optional[str] = Field(None)
    owner_id: str = Field(...)
    
    class Config:
        collection_name = "acm_movie_collections"
        indexes = [
            {"key": [("title", 1), ("owner_id", 1)], "unique": True},
            {"key": [("owner_id", 1)]}
        ] 