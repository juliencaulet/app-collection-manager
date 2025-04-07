from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class MovieCollection(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    total_movies: Optional[int] = None
    status: str = "ongoing"  # ongoing, completed, cancelled
    movie_ids: List[str] = []
    notes: Optional[str] = None
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "acm_movie_collections"
        json_schema_extra = {
            "example": {
                "name": "The Lord of the Rings",
                "description": "Epic fantasy film series",
                "genre": "Fantasy",
                "total_movies": 3,
                "status": "completed",
                "tags": ["fantasy", "epic"]
            }
        }
        populate_by_name = True
