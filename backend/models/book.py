from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class Book(BaseDBModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    publication_year: Optional[int] = Field(None, ge=1000, le=2100)
    publisher: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)
    genres: List[str] = Field(default_factory=list)
    series_id: Optional[str] = Field(None)
    series_order: Optional[int] = Field(None, ge=1)
    cover_image_url: Optional[str] = Field(None)
    owner_id: str = Field(...)
    
    class Config:
        collection_name = "acm_books"
        indexes = [
            {"key": [("title", 1), ("author", 1)], "unique": True},
            {"key": [("isbn", 1)], "unique": True, "sparse": True},
            {"key": [("owner_id", 1)]},
            {"key": [("series_id", 1)]}
        ] 