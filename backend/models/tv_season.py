from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseDBModel

class TVSeasonBase(BaseModel):
    show_id: str = Field(..., description="ID of the TV show this season belongs to")
    season_number: int = Field(..., ge=1, description="Season number (1-based)")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    air_date: Optional[datetime] = None
    episodes_count: int = Field(0, ge=0)
    poster_url: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    tmdb_id: Optional[int] = None

class TVSeasonCreate(TVSeasonBase):
    pass

class TVSeasonUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    air_date: Optional[datetime] = None
    episodes_count: Optional[int] = Field(None, ge=0)
    poster_url: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    tmdb_id: Optional[int] = None

class TVSeasonInDB(TVSeasonBase, BaseDBModel):
    pass

class TVSeason(TVSeasonBase):
    id: str
    created_at: datetime
    updated_at: datetime 