import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

try:
    from api.routes import books, movies, book_series, movie_collections, users
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Python path: {sys.path}") 