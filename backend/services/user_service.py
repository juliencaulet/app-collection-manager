from typing import Optional
from fastapi import HTTPException
from models.user import User
from core.database import get_database
from core.security import get_password_hash, verify_password
from datetime import datetime

class UserService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db[User.Config.collection_name]

    async def create_user(self, user: User) -> User:
        """Create a new user with hashed password."""
        try:
            # Check if username or email already exists
            if await self.collection.find_one({"username": user.username}):
                raise HTTPException(status_code=400, detail="Username already registered")
            if await self.collection.find_one({"email": user.email}):
                raise HTTPException(status_code=400, detail="Email already registered")

            # Hash the password
            user.password = get_password_hash(user.password.get_secret_value())
            
            result = await self.collection.insert_one(user.dict())
            user.id = str(result.inserted_id)
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        user = await self.collection.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        user = await self.collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        user = await self.collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**user)

    async def update_user(self, user_id: str, user: User) -> User:
        """Update a user."""
        user.updated_at = datetime.utcnow()
        
        # If password is being updated, hash it
        if user.password:
            user.password = get_password_hash(user.password.get_secret_value())

        result = await self.collection.update_one(
            {"_id": user_id},
            {"$set": user.dict(exclude={"id"})}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        result = await self.collection.delete_one({"_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return True

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password.get_secret_value()):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.update_user(user.id, user)
        return user
