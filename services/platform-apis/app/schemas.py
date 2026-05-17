"""
Pydantic schemas for Platform APIs Service
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Platform(str, Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"

class UploadRequest(BaseModel):
    """Request model for content upload"""
    content_id: str = Field(..., description="Content ID to upload")
    video_url: str = Field(..., description="URL to video file")
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    platforms: List[Platform] = Field(..., description="Target platforms")
    tags: Optional[List[str]] = Field(None, description="Video tags")
    category_id: Optional[str] = Field(None, description="YouTube category ID")
    privacy_level: Optional[str] = Field("public", description="Privacy level")
    access_token: Optional[str] = Field(None, description="Platform access token")
    thumbnail_url: Optional[str] = Field(None, description="Custom thumbnail URL")

class UploadResponse(BaseModel):
    """Response model for upload initiation"""
    upload_id: str = Field(..., description="Unique upload identifier")
    status: str = Field(..., description="Upload status")
    message: str = Field(..., description="Status message")

class UploadStatus(BaseModel):
    """Model for upload status"""
    upload_id: str = Field(..., description="Unique upload identifier")
    status: str = Field(..., description="Overall upload status")
    platforms: Dict[str, Dict[str, Any]] = Field(..., description="Platform-specific status")
    error_message: Optional[str] = Field(None, description="Error message if failed")

class PlatformCredentials(BaseModel):
    """Model for platform credentials"""
    platform: Platform = Field(..., description="Platform name")
    access_token: str = Field(..., description="OAuth access token")
    refresh_token: Optional[str] = Field(None, description="OAuth refresh token")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")
    user_id: Optional[str] = Field(None, description="Platform user ID")

class ScheduleRequest(BaseModel):
    """Request model for scheduled uploads"""
    content_id: str = Field(..., description="Content ID to upload")
    video_url: str = Field(..., description="URL to video file")
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    platforms: List[Platform] = Field(..., description="Target platforms")
    schedule_time: datetime = Field(..., description="Scheduled upload time")
    timezone: str = Field(default="UTC", description="Timezone for schedule")
    tags: Optional[List[str]] = Field(None, description="Video tags")
    category_id: Optional[str] = Field(None, description="YouTube category ID")
    privacy_level: Optional[str] = Field("public", description="Privacy level")

class PlatformAnalytics(BaseModel):
    """Model for platform analytics"""
    platform: Platform = Field(..., description="Platform name")
    video_id: str = Field(..., description="Platform video ID")
    views: int = Field(default=0, description="View count")
    likes: int = Field(default=0, description="Like count")
    comments: int = Field(default=0, description="Comment count")
    shares: int = Field(default=0, description="Share count")
    engagement_rate: float = Field(default=0.0, description="Engagement rate")
    revenue: float = Field(default=0.0, description="Revenue generated")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update time")



