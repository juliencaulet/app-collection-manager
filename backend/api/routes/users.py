from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from models.user import User
from services.user_service import UserService
from utils.security import get_current_user, create_access_token

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=User)
async def create_user(user: User, service: UserService = Depends()):
    """Create a new user."""
    return await service.create_user(user)

@router.get("/me", response_model=User)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, service: UserService = Depends(), current_user = Depends(get_current_user)):
    """Get a user by ID."""
    return await service.get_user(user_id)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User, service: UserService = Depends(), current_user = Depends(get_current_user)):
    """Update a user."""
    return await service.update_user(user_id, user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, service: UserService = Depends(), current_user = Depends(get_current_user)):
    """Delete a user."""
    return await service.delete_user(user_id)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends()):
    """Login and get access token."""
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
