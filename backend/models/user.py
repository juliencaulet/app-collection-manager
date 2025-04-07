"""
User model for the application.

This module defines the User model and its configuration for MongoDB storage.
The User model represents a user in the system and includes fields for:
- User identification (username, email, full name)
- Authentication (password, login tracking)
- Authorization (roles, account status)
- User preferences and settings

The model includes comprehensive validation and indexing for efficient querying.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import Field, EmailStr, constr
from .base import BaseDBModel, MongoDBConfig

class User(BaseDBModel):
    """
    User model representing a user in the system.
    
    This model includes fields for user identification, authentication, and authorization.
    It extends BaseDBModel to include standard fields for document identification and audit tracking.
    
    Attributes:
        username (str): Unique username for the user (3-50 characters)
        email (EmailStr): User's email address
        full_name (str): User's full name (1-100 characters)
        disabled (bool): Whether the user account is disabled
        hashed_password (str): Hashed password for the user
        roles (List[str]): List of roles assigned to the user
        last_login (Optional[datetime]): Timestamp of the user's last login
        failed_login_attempts (int): Number of consecutive failed login attempts
        account_locked_until (Optional[datetime]): Timestamp until which the account is locked
        preferences (dict): User preferences and settings
    """
    username: constr(min_length=3, max_length=50) = Field(
        description="Unique username for the user"
    )
    email: EmailStr = Field(
        description="User's email address"
    )
    full_name: constr(min_length=1, max_length=100) = Field(
        description="User's full name"
    )
    disabled: bool = Field(
        default=False,
        description="Whether the user account is disabled"
    )
    hashed_password: str = Field(
        description="Hashed password for the user"
    )
    roles: List[str] = Field(
        default=["user"],
        description="List of roles assigned to the user"
    )
    last_login: Optional[datetime] = Field(
        default=None,
        description="Timestamp of the user's last login"
    )
    failed_login_attempts: int = Field(
        default=0,
        description="Number of consecutive failed login attempts"
    )
    account_locked_until: Optional[datetime] = Field(
        default=None,
        description="Timestamp until which the account is locked"
    )
    preferences: dict = Field(
        default_factory=dict,
        description="User preferences and settings"
    )

    class Config(MongoDBConfig):
        """
        Configuration for the User model.
        
        This class defines the MongoDB collection name and indexes for the User model.
        The indexes are designed to optimize common queries and ensure data integrity.
        
        Attributes:
            collection_name (str): Name of the MongoDB collection
            indexes (List[Dict[str, Any]]): List of index configurations
        """
        collection_name = "users"
        indexes = [
            {"key": {"username": 1}, "unique": True},
            {"key": {"email": 1}, "unique": True},
            {"key": {"roles": 1}},
            {"key": {"last_login": 1}},
            {"key": {"created_at": 1}},
            {"key": {"updated_at": 1}}
        ] 