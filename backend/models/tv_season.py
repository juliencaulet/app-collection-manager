from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class TVSeason(BaseDBModel):
    tv_show_id: str = Field(...)
    season_number: int = Field(..., ge=1)
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    release_year: Optional[int] = Field(None, ge=1928, le=2100)
    total_episodes: int = Field(default=0, ge=0)
    poster_url: Optional[str] = Field(None)
    owner_id: str = Field(...)
    
    class Config:
        collection_name = "acm_tv_seasons"
        indexes = [
            {"key": [("tv_show_id", 1), ("season_number", 1)], "unique": True},
            {"key": [("owner_id", 1)]}
        ] 