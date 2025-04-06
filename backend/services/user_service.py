"""
User service for handling user-related operations.
"""

import logging
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from models.user import User
from core.errors import CollectionManagerError

# Get module-specific logger
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[User.Config.collection_name]

    async def create_user(self, user: User) -> User:
        """
        Create a new user.
        
        Args:
            user: User object to create
            
        Returns:
            Created user object
            
        Raises:
            CollectionManagerError: If user creation fails
        """
        try:
            # Check if username or email already exists
            existing_user = await self.collection.find_one({
                "$or": [
                    {"username": user.username},
                    {"email": user.email}
                ]
            })
            
            if existing_user:
                raise CollectionManagerError(
                    status_code=400,
                    detail="Username or email already exists"
                )
            
            # Insert new user
            user_dict = user.model_dump()
            result = await self.collection.insert_one(user_dict)
            if not result.inserted_id:
                raise CollectionManagerError(
                    status_code=500,
                    detail="Failed to create user"
                )
                
            # Get the created user directly from the database
            created_user_data = await self.collection.find_one({"_id": result.inserted_id})
            if not created_user_data:
                raise CollectionManagerError(
                    status_code=500,
                    detail="Failed to retrieve created user"
                )
                
            # Convert ObjectId to string for the response
            created_user_data["id"] = str(created_user_data.pop("_id"))
            return User(**created_user_data)
        except CollectionManagerError:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise CollectionManagerError(
                status_code=500,
                detail=f"Error creating user: {str(e)}"
            )

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID to retrieve (MongoDB ObjectId)
            
        Returns:
            User object if found, None otherwise
        """
        try:
            user_data = await self.collection.find_one({"_id": user_id})
            if user_data:
                # Convert ObjectId to string for the response
                user_data["id"] = str(user_data.pop("_id"))
                return User(**user_data)
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            return None

    async def get_all_users(self) -> List[User]:
        """
        Get all users.
        
        Returns:
            List of user objects
        """
        try:
            users = []
            async for user_data in self.collection.find():
                # Convert ObjectId to string for the response
                user_data["id"] = str(user_data.pop("_id"))
                users.append(User(**user_data))
            return users
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        """
        Update a user.
        
        Args:
            user_id: User ID to update
            user_data: Dictionary containing fields to update
            
        Returns:
            Updated user object if successful, None otherwise
            
        Raises:
            CollectionManagerError: If update fails
        """
        try:
            # Convert string ID to ObjectId
            try:
                user_id_obj = ObjectId(user_id)
            except Exception:
                raise CollectionManagerError(
                    status_code=400,
                    detail="Invalid user ID format"
                )

            # Check if user exists
            existing_user = await self.get_user_by_id(user_id_obj)
            if not existing_user:
                return None

            # Check if new username or email conflicts with other users
            if "username" in user_data or "email" in user_data:
                query = {
                    "$or": [],
                    "_id": {"$ne": user_id_obj}  # Exclude current user
                }
                if "username" in user_data:
                    query["$or"].append({"username": user_data["username"]})
                if "email" in user_data:
                    query["$or"].append({"email": user_data["email"]})
                
                if query["$or"]:  # Only check if we have fields to check
                    conflict = await self.collection.find_one(query)
                    if conflict:
                        raise CollectionManagerError(
                            status_code=400,
                            detail="Username or email already exists"
                        )

            # Update user
            result = await self.collection.update_one(
                {"_id": user_id_obj},
                {"$set": user_data}
            )
            
            if result.modified_count == 0:
                return None
                
            # Get the updated user directly from the database
            updated_user_data = await self.collection.find_one({"_id": user_id_obj})
            if updated_user_data:
                # Convert ObjectId to string for the response
                updated_user_data["id"] = str(updated_user_data.pop("_id"))
                return User(**updated_user_data)
            return None
        except CollectionManagerError:
            raise
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise CollectionManagerError(
                status_code=500,
                detail=f"Error updating user: {str(e)}"
            )

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if user was deleted, False otherwise
        """
        try:
            # Convert string ID to ObjectId
            try:
                user_id_obj = ObjectId(user_id)
            except Exception:
                return False

            result = await self.collection.delete_one({"_id": user_id_obj})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return False 