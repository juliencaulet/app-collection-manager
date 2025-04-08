from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .base import BaseDBModel

class TVShowBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    release_year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    genres: List[str] = Field(default_factory=list)
    rating: Optional[float] = Field(None, ge=0, le=10)
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
    status: str = Field(..., description="Current status of the show (e.g., 'Ended', 'Ongoing', 'Cancelled')")
    network: Optional[str] = None
    seasons_count: int = Field(0, ge=0)
    episodes_count: int = Field(0, ge=0)
    last_air_date: Optional[datetime] = None
    next_air_date: Optional[datetime] = None

class TVShowCreate(TVShowBase):
    pass

class TVShowUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    release_year: Optional[int] = Field(None, ge=1900, le=datetime.now().year)
    genres: Optional[List[str]] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
    status: Optional[str] = None
    network: Optional[str] = None
    seasons_count: Optional[int] = Field(None, ge=0)
    episodes_count: Optional[int] = Field(None, ge=0)
    last_air_date: Optional[datetime] = None
    next_air_date: Optional[datetime] = None

class TVShowInDB(TVShowBase, BaseDBModel):
    pass

class TVShow(TVShowBase):
    id: str
    created_at: datetime
    updated_at: datetime 