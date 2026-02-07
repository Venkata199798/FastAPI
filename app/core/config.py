
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    English: Application settings loaded from environment variables
    Telugu: పర్యావరణ వేరియబుల్స్ నుండి లోడ్ చేయబడిన అప్లికేషన్ సెట్టింగ్స్
    """
  
    DATABASE_URL: str
    
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    PROJECT_NAME: str = "Student Management System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
   
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()