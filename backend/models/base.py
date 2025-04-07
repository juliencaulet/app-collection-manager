"""
Base model for MongoDB documents.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BaseDBModel(BaseModel):
    """
    Base model for all database models.
    """
    id: Optional[str] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 