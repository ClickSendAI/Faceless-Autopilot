"""
Configuration settings for AI Content Service
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
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    PEXELS_API_KEY: str = os.getenv("PEXELS_API_KEY", "")
    
    # Service URLs
    PLATFORM_APIS_URL: str = "http://localhost:8562"
    ANALYTICS_URL: str = "http://localhost:8563"
    USER_MANAGEMENT_URL: str = "http://localhost:8004"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    GENERATED_CONTENT_DIR: str = "generated_content"
    
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
