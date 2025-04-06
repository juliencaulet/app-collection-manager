from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class TVShow(BaseDBModel):
    title: str = Field(..., min_length=1, max_length=200)
    original_title: Optional[str] = Field(None, max_length=200)
    start_year: Optional[int] = Field(None, ge=1928, le=2100)  # First TV show was in 1928
    end_year: Optional[int] = Field(None, ge=1928, le=2100)
    creators: List[str] = Field(default_factory=list)
    description: Optional[str] = Field(None, max_length=2000)
    genres: List[str] = Field(default_factory=list)
    imdb_id: Optional[str] = Field(None, min_length=9, max_length=9)  # tt + 7 digits
    total_seasons: int = Field(default=0, ge=0)
    poster_url: Optional[str] = Field(None)
    owner_id: str = Field(...)
    
    class Config:
        collection_name = "acm_tv_shows"
        indexes = [
            {"key": [("title", 1), ("start_year", 1)], "unique": True},
            {"key": [("imdb_id", 1)], "unique": True, "sparse": True},
            {"key": [("owner_id", 1)]}
        ] 