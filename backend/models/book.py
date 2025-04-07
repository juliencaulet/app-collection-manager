"""
Book model for the application.

This module defines the Book model and its configuration for MongoDB storage.
The Book model represents a book in the system and includes fields for:
- Book identification (title, isbn, author)
- Publication details (publisher, publication_date)
- Physical attributes (pages, dimensions)
- Classification (genre, language)
- Collection management (series, status)
- Content information (synopsis, cover)

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import Optional, List
from datetime import date, datetime
from pydantic import Field, constr, HttpUrl
from .base import BaseDBModel, MongoDBConfig
from .common import PyObjectId
from bson import ObjectId

class Book(BaseDBModel):
    """
    Book model representing a book in the system.
    
    This model includes fields for book identification, publication details, and collection management.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        title (str): Title of the book (1-200 characters)
        original_title (Optional[str]): Original title in the book's language
        author (str): Author of the book (1-100 characters)
        isbn (Optional[str]): International Standard Book Number
        publisher (Optional[str]): Publisher of the book
        year (int): Publication year
        pages (Optional[int]): Number of pages
        genre (List[str]): List of genres the book belongs to
        format (str): Format of the book (e.g., Hardcover, Paperback)
        language (str): Language of the book
        collection_id (Optional[PyObjectId]): ID of the book collection this book belongs to
        status (str): Current status of the book (e.g., owned, wanted)
        notes (Optional[str]): Additional notes about the book
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: constr(min_length=1, max_length=200) = Field(
        description="Title of the book"
    )
    original_title: Optional[str] = Field(
        default=None,
        description="Original title in the book's language"
    )
    author: constr(min_length=1, max_length=100) = Field(
        description="Author of the book"
    )
    isbn: Optional[str] = Field(
        default=None,
        description="International Standard Book Number",
        pattern=r"^(?:ISBN[- ])?(?:[0-9]{10}|[0-9]{13})$"
    )
    publisher: Optional[str] = Field(
        default=None,
        description="Publisher of the book"
    )
    year: int = Field(
        description="Publication year",
        ge=868  # First printed book
    )
    pages: Optional[int] = Field(
        default=None,
        description="Number of pages",
        ge=1
    )
    genre: List[str] = Field(
        default_factory=list,
        description="List of genres the book belongs to"
    )
    format: str = Field(
        description="Format of the book (e.g., Hardcover, Paperback)"
    )
    language: str = Field(
        description="Language of the book"
    )
    collection_id: Optional[PyObjectId] = Field(
        default=None,
        description="ID of the book collection this book belongs to"
    )
    status: str = Field(
        default="owned",
        description="Current status of the book (e.g., owned, wanted)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the book"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config(MongoDBConfig):
        """
        Configuration for the Book model.
        
        This class defines the MongoDB collection name and indexes for the Book model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "books"
        indexes = [
            {"key": {"title": 1}, "name": "title_idx"},
            {"key": {"author": 1}, "name": "author_idx"},
            {"key": {"isbn": 1}, "name": "isbn_idx", "unique": True, "sparse": True},
            {"key": {"year": 1}, "name": "year_idx"},
            {"key": {"genre": 1}, "name": "genre_idx"},
            {"key": {"collection_id": 1}, "name": "collection_id_idx"},
            {"key": {"status": 1}, "name": "status_idx"},
            {"key": {"created_at": 1}, "name": "created_at_idx"},
            {"key": {"updated_at": 1}, "name": "updated_at_idx"}
        ]
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "978-0743273565",
                "year": 1925,
                "genre": ["Fiction", "Classic"],
                "format": "Paperback",
                "language": "English",
                "collection_id": "507f1f77bcf86cd799439011"
            }
        } 