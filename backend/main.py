"""
Main FastAPI application entry point.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import books, movies, book_series, movie_collections, users
from config.environment import get_debug, get_cors_origins, get_environment

app = FastAPI(
    title=f"App Collection Manager API ({get_environment().title()})",
    description="API for managing book and movie collections",
    version="1.0.0",
    debug=get_debug()
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(books.router)
app.include_router(movies.router)
app.include_router(book_series.router)
app.include_router(movie_collections.router)

@app.get("/")
async def root():
    return {"message": "Welcome to App Collection Manager API"} 