"""
Book routes for the Collection Manager API.

This module provides endpoints for managing books in the system,
including adding new books, updating existing ones, and handling
scraped book data from various sources.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import date

from core.auth import get_current_user
from models.user import User
from services.book_service import add_scraped_album, update_book, delete_book
from core.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

@router.post("/scrape", response_model=Dict[str, Any])
async def scrape_and_add_book(
    url: str,
    download_cover: bool = True,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Scrape a book from BubbleBD and add it to the database.
    
    Args:
        url: URL of the book on BubbleBD
        download_cover: Whether to download and save the cover image
        current_user: Currently authenticated user
        db: Database instance
        
    Returns:
        Dict[str, Any]: The newly created book document
        
    Raises:
        HTTPException: If the book cannot be scraped or added
    """
    try:
        book = await add_scraped_album(db, url, str(current_user.id), download_cover)
        return book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add book: {str(e)}"
        )

@router.put("/{book_id}", response_model=Dict[str, Any])
async def update_existing_book(
    book_id: str,
    update_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update an existing book in the database.
    
    Args:
        book_id: ID of the book to update
        update_data: Dictionary of fields to update
        current_user: Currently authenticated user
        db: Database instance
        
    Returns:
        Dict[str, Any]: The updated book document
        
    Raises:
        HTTPException: If the book cannot be found or updated
    """
    try:
        book = await update_book(db, book_id, update_data, str(current_user.id))
        return book
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book: {str(e)}"
        )

@router.delete("/{book_id}")
async def remove_book(
    book_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Delete a book from the database.
    
    Args:
        book_id: ID of the book to delete
        current_user: Currently authenticated user
        db: Database instance
        
    Returns:
        Dict[str, str]: Success message
        
    Raises:
        HTTPException: If the book cannot be found or deleted
    """
    try:
        await delete_book(db, book_id, str(current_user.id))
        return {"message": "Book deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete book: {str(e)}"
        ) 