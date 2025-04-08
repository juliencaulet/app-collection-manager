from fastapi import APIRouter
from .books import router as books_router
from .book_series import router as book_series_router
from .movies import router as movies_router
from .movie_collections import router as movie_collections_router
from .tv_shows import router as tv_shows_router
from .tv_seasons import router as tv_seasons_router
from .users import router as users_router
from .system import router as system_router

router = APIRouter()

router.include_router(books_router)
router.include_router(book_series_router)
router.include_router(movies_router)
router.include_router(movie_collections_router)
router.include_router(tv_shows_router)
router.include_router(tv_seasons_router)
router.include_router(users_router)
router.include_router(system_router) 