"""
Book Series model for the application.

This module defines the BookSeries model and its configuration for MongoDB storage.
The BookSeries model represents a series of books in the system and includes fields for:
- Series identification (title, description)
- Series management (total books, status)
- Classification (genre, language)
- Collection management (status, notes)

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import Optional, List
from pydantic import Field, constr
from .base import BaseDBModel, MongoDBConfig

class BookSeries(BaseDBModel):
    """
    Book Series model representing a series of books in the system.
    
    This model includes fields for series identification, management, and classification.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        title (str): Title of the series (1-200 characters)
        description (Optional[str]): Description of the series
        total_books (Optional[int]): Total number of books in the series
        current_book (Optional[int]): Current book number in the series
        genre (List[str]): List of genres the series belongs to
        language (str): Language of the series
        status (str): Current status of the series (e.g., ongoing, completed)
        notes (Optional[str]): Additional notes about the series
    """
    title: constr(min_length=1, max_length=200) = Field(
        description="Title of the series"
    )
    description: Optional[str] = Field(
        default=None,
        description="Description of the series"
    )
    total_books: Optional[int] = Field(
        default=None,
        description="Total number of books in the series",
        ge=1
    )
    current_book: Optional[int] = Field(
        default=None,
        description="Current book number in the series",
        ge=1
    )
    genre: List[str] = Field(
        default_factory=list,
        description="List of genres the series belongs to"
    )
    language: str = Field(
        description="Language of the series"
    )
    status: str = Field(
        default="ongoing",
        description="Current status of the series (e.g., ongoing, completed)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the series"
    )

    class Config(MongoDBConfig):
        """
        Configuration for the BookSeries model.
        
        This class defines the MongoDB collection name and indexes for the BookSeries model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "book_series"
        indexes = [
            {"key": {"title": 1}, "unique": True},
            {"key": {"genre": 1}},
            {"key": {"status": 1}},
            {"key": {"created_at": 1}},
            {"key": {"updated_at": 1}}
        ] 