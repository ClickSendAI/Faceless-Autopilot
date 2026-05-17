"""
Pydantic schemas for AI Content Generation Service
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ContentFormat(str, Enum):
    SHORT = "short"  # 15-60 seconds
    MEDIUM = "medium"  # 1-3 minutes
    LONG = "long"  # 3-10 minutes

class Platform(str, Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"

class ContentRequest(BaseModel):
    """Request model for content generation"""
    topic: str = Field(..., description="Content topic or theme")
    niche: str = Field(..., description="Content niche (e.g., productivity, tech, lifestyle)")
    format: ContentFormat = Field(..., description="Content format/duration")
    duration: int = Field(default=60, description="Duration in seconds")
    voice_id: str = Field(default="default", description="ElevenLabs voice ID")
    platforms: List[Platform] = Field(..., description="Target platforms")
    style: Optional[str] = Field(None, description="Content style (e.g., educational, entertaining)")
    tone: Optional[str] = Field(None, description="Content tone (e.g., professional, casual)")

class ContentResponse(BaseModel):
    """Response model for content generation"""
    content_id: str = Field(..., description="Unique content identifier")
    status: str = Field(..., description="Generation status")
    message: str = Field(..., description="Status message")

class ContentStatus(BaseModel):
    """Model for content generation status"""
    content_id: str = Field(..., description="Unique content identifier")
    status: str = Field(..., description="Current status (processing, completed, failed)")
    progress: int = Field(..., description="Progress percentage (0-100)")
    video_url: Optional[str] = Field(None, description="URL to generated video")
    error_message: Optional[str] = Field(None, description="Error message if failed")

class ScriptGenerationRequest(BaseModel):
    """Request for script generation only"""
    topic: str = Field(..., description="Script topic")
    niche: str = Field(..., description="Content niche")
    format: ContentFormat = Field(..., description="Content format")
    duration: int = Field(default=60, description="Duration in seconds")
    style: Optional[str] = Field(None, description="Script style")
    tone: Optional[str] = Field(None, description="Script tone")

class VoiceGenerationRequest(BaseModel):
    """Request for voice generation only"""
    text: str = Field(..., description="Text to convert to speech")
    voice_id: str = Field(default="default", description="ElevenLabs voice ID")
    speed: float = Field(default=1.0, description="Speech speed multiplier")

class VideoAssemblyRequest(BaseModel):
    """Request for video assembly"""
    script: str = Field(..., description="Script text")
    voice_url: str = Field(..., description="URL to voice file")
    format: ContentFormat = Field(..., description="Video format")
    platforms: List[Platform] = Field(..., description="Target platforms")
    background_music: Optional[str] = Field(None, description="Background music URL")



