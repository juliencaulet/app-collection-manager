"""
Book model for the application.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    author: str
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
    cover_image: Optional[str] = None
    genre: Optional[str] = None
    status: str = "unread"  # unread, reading, read
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    series_id: Optional[str] = None
    series_order: Optional[int] = None
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "acm_books"
        json_schema_extra = {
            "example": {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "isbn": "9780547928227",
                "publisher": "Houghton Mifflin Harcourt",
                "description": "A great fantasy novel",
                "page_count": 366,
                "language": "English",
                "genre": "Fantasy",
                "status": "unread",
                "tags": ["fantasy", "adventure"]
            }
        }
        populate_by_name = True
        indexes = [
            {"key": [("title", 1)]},
            {"key": [("author", 1)]},
            {"key": [("isbn", 1)], "unique": True, "sparse": True},
            {"key": [("genre", 1)]},
            {"key": [("status", 1)]},
            {"key": [("series_id", 1)]},
            {"key": [("tags", 1)]}
        ] 