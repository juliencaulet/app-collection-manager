from .base import Settings

class DevelopmentSettings(Settings):
    DEBUG: bool = True
    
    # Development-specific MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "acm_dev"
    
    # Development-specific CORS settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8001",
        "http://127.0.0.1:8001"
    ]
    
    class Config:
        env_file = ".env.development"
        case_sensitive = True 