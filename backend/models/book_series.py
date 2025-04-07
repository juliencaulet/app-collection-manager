from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class BookSeries(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    author: str
    description: Optional[str] = None
    genre: Optional[str] = None
    total_books: Optional[int] = None
    status: str = "ongoing"  # ongoing, completed, cancelled
    book_ids: List[str] = []
    notes: Optional[str] = None
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        collection_name = "acm_book_series"
        json_schema_extra = {
            "example": {
                "name": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "description": "Epic high-fantasy novel series",
                "genre": "Fantasy",
                "total_books": 3,
                "status": "completed",
                "tags": ["fantasy", "classic"]
            }
        }
        populate_by_name = True
