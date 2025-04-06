"""
User API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from models.user import User
from services.user_service import UserService
from core.database import database

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service() -> UserService:
    """Get user service instance."""
    return UserService(database.db)

@router.post("/", response_model=User)
async def create_user(user: User, user_service: UserService = Depends(get_user_service)):
    """
    Create a new user.
    
    Args:
        user: User data to create
        user_service: User service instance
        
    Returns:
        Created user object
    """
    try:
        return await user_service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[User])
async def get_users(user_service: UserService = Depends(get_user_service)):
    """
    Get all users.
    
    Args:
        user_service: User service instance
        
    Returns:
        List of users
    """
    return await user_service.get_all_users()

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    """
    Get user by ID.
    
    Args:
        user_id: User ID to retrieve
        user_service: User service instance
        
    Returns:
        User object
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_data: Dict[str, Any],
    user_service: UserService = Depends(get_user_service)
):
    """
    Update a user.
    
    Args:
        user_id: User ID to update
        user_data: Dictionary containing fields to update
        user_service: User service instance
        
    Returns:
        Updated user object
    """
    try:
        updated_user = await user_service.update_user(user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: str, user_service: UserService = Depends(get_user_service)):
    """
    Delete a user.
    
    Args:
        user_id: User ID to delete
        user_service: User service instance
        
    Returns:
        Success message
    """
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"} 