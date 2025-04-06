from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class BookSeries(BaseDBModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)
    genres: List[str] = Field(default_factory=list)
    total_books: int = Field(default=0, ge=0)
    cover_image_url: Optional[str] = Field(None)
    owner_id: str = Field(...)
    
    class Config:
        collection_name = "acm_book_series"
        indexes = [
            {"key": [("title", 1), ("author", 1)], "unique": True},
            {"key": [("owner_id", 1)]}
        ] 