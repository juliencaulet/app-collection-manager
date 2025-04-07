"""
Book model for the application.
"""

from typing import Optional, List
from pydantic import Field
from .base import BaseDBModel

class Book(BaseDBModel):
    """
    Book model representing a book in the system.
    """
    title: str = Field(description="Title of the book")
    author: str = Field(description="Author of the book")
    isbn: Optional[str] = Field(default=None, description="International Standard Book Number")
    year: int = Field(description="Publication year")
    genre: List[str] = Field(default_factory=list, description="List of genres")
    status: str = Field(default="owned", description="Current status of the book")
    notes: Optional[str] = Field(default=None, description="Additional notes") 