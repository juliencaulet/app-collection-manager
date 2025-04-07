"""
Book service module for the Collection Manager application.

This module provides functions for managing books in the database,
including adding new books, updating existing ones, and handling
scraped book data from various sources.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from models.book import Book
from models.book_series import BookSeries
from scrapers.bubblebd.albums import BubbleBDScraper, BubbleBDAlbum
from bson import ObjectId

# Configure logging
logger = logging.getLogger(__name__)

async def add_scraped_album(
    db: AsyncIOMotorDatabase,
    url: str,
    user_id: str,
    download_cover: bool = True
) -> Book:
    """
    Scrape a book album from BubbleBD and add it to the database.
    
    Args:
        db: AsyncIOMotorDatabase instance
        url: URL of the album on BubbleBD
        user_id: ID of the user adding the book
        download_cover: Whether to download and save the cover image
        
    Returns:
        Book: The newly created book document
        
    Raises:
        ValueError: If the album cannot be scraped or added to the database
    """
    try:
        # Initialize scraper and get album data
        scraper = BubbleBDScraper()
        album = scraper.scrape_album(url, download_cover=download_cover)
        
        # Check if series exists, create if not
        series = None
        if album.series_title:
            series = await db.book_series.find_one({"title": album.series_title})
            if not series:
                series = await db.book_series.insert_one({
                    "title": album.series_title,
                    "total_books": album.total_volumes,
                    "current_book": album.series_number,
                    "genre": album.genre,
                    "language": album.language,
                    "status": "ongoing",
                    "notes": f"Series imported from BubbleBD",
                    "created_by": user_id,
                    "updated_by": user_id,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                })
                series_id = series.inserted_id
            else:
                series_id = series["_id"]
                # Update series if needed
                if album.total_volumes and album.total_volumes != series.get("total_books"):
                    await db.book_series.update_one(
                        {"_id": series_id},
                        {
                            "$set": {
                                "total_books": album.total_volumes,
                                "updated_by": user_id,
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
        
        # Create book document
        book_data = {
            "title": album.title,
            "isbn": album.isbn,
            "author": ", ".join(album.authors),  # Join multiple authors
            "publisher": album.publisher,
            "publication_date": datetime.strptime(album.publication_date, "%Y-%m-%d").date(),
            "pages": album.pages,
            "genre": album.genre,
            "language": album.language,
            "series_id": series_id if series else None,
            "series_number": album.series_number,
            "status": album.status,
            "notes": album.notes,
            "cover_url": album.cover_url,
            "synopsis": album.synopsis,
            "created_by": user_id,
            "updated_by": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert book into database
        result = await db.books.insert_one(book_data)
        if not result.inserted_id:
            raise ValueError("Failed to insert book into database")
            
        # Return the newly created book
        return await db.books.find_one({"_id": result.inserted_id})
    except Exception as e:
        logger.error(f"Error adding scraped album: {str(e)}")
        raise ValueError(f"Failed to add scraped album: {str(e)}")

async def update_book(
    db: AsyncIOMotorDatabase,
    book_id: str,
    update_data: Dict[str, Any],
    user_id: str
) -> Book:
    """
    Update an existing book in the database.
    
    Args:
        db: AsyncIOMotorDatabase instance
        book_id: ID of the book to update
        update_data: Dictionary of fields to update
        user_id: ID of the user making the update
        
    Returns:
        Book: The updated book document
        
    Raises:
        ValueError: If the book cannot be found or updated
    """
    try:
        # Add audit fields
        update_data["updated_by"] = user_id
        update_data["updated_at"] = datetime.utcnow()
        
        # Convert string dates to datetime objects if present
        if "publication_date" in update_data:
            update_data["publication_date"] = datetime.strptime(
                update_data["publication_date"], "%Y-%m-%d"
            ).date()
        
        # Update the book
        result = await db.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise ValueError("Book not found or no changes made")
            
        # Return the updated book
        return await db.books.find_one({"_id": ObjectId(book_id)})
    except Exception as e:
        logger.error(f"Error updating book: {str(e)}")
        raise ValueError(f"Failed to update book: {str(e)}")

async def delete_book(
    db: AsyncIOMotorDatabase,
    book_id: str,
    user_id: str
) -> bool:
    """
    Delete a book from the database.
    
    Args:
        db: AsyncIOMotorDatabase instance
        book_id: ID of the book to delete
        user_id: ID of the user making the deletion
        
    Returns:
        bool: True if the book was deleted successfully
        
    Raises:
        ValueError: If the book cannot be found or deleted
    """
    try:
        # First check if the book exists
        book = await db.books.find_one({"_id": ObjectId(book_id)})
        if not book:
            raise ValueError("Book not found")
            
        # Delete the book
        result = await db.books.delete_one({"_id": ObjectId(book_id)})
        
        if result.deleted_count == 0:
            raise ValueError("Failed to delete book")
            
        # If the book was part of a series, update the series
        if book.get("series_id"):
            # Check if this was the last book in the series
            remaining_books = await db.books.count_documents({
                "series_id": book["series_id"]
            })
            
            if remaining_books == 0:
                # Delete the series if no books remain
                await db.book_series.delete_one({"_id": book["series_id"]})
            else:
                # Update the series' current_book if needed
                series = await db.book_series.find_one({"_id": book["series_id"]})
                if series and series.get("current_book") == book.get("series_number"):
                    # Find the next highest book number in the series
                    next_book = await db.books.find_one(
                        {"series_id": book["series_id"]},
                        sort=[("series_number", -1)]
                    )
                    if next_book:
                        await db.book_series.update_one(
                            {"_id": book["series_id"]},
                            {
                                "$set": {
                                    "current_book": next_book["series_number"],
                                    "updated_by": user_id,
                                    "updated_at": datetime.utcnow()
                                }
                            }
                        )
        
        return True
    except Exception as e:
        logger.error(f"Error deleting book: {str(e)}")
        raise ValueError(f"Failed to delete book: {str(e)}") 