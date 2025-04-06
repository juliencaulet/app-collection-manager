from typing import Optional, List
from pydantic import EmailStr, Field
from .base import BaseDBModel

class User(BaseDBModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    disabled: bool = Field(default=False)
    hashed_password: str
    roles: List[str] = Field(default=["user"])
    
    class Config:
        collection_name = "acm_users"
        indexes = [
            {"key": [("username", 1)], "unique": True},
            {"key": [("email", 1)], "unique": True}
        ] 