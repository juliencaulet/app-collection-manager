import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.absolute()

# Add the project root to Python path if it's not already there
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True) 