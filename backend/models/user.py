from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    email: EmailStr
    password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        collection_name = "acm_users"
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "secretpassword",
                "is_active": True,
                "is_superuser": False
            }
        }
        populate_by_name = True 