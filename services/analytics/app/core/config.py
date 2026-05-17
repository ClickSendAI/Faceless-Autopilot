"""
Configuration settings for Analytics Service
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:tjq5uxt3@localhost:5432/faceless_autopilot_ai"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Service URLs
    AI_CONTENT_URL: str = "http://localhost:8561"
    PLATFORM_APIS_URL: str = "http://localhost:8562"
    USER_MANAGEMENT_URL: str = "http://localhost:8004"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
