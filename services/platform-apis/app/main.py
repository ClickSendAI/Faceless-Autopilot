"""
Platform APIs Service
Handles content uploads to YouTube, TikTok, Instagram, and other platforms
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import logging
from datetime import datetime
import uuid

from .schemas import UploadRequest, UploadResponse, UploadStatus
from .services.youtube_service import YouTubeService
from .services.tiktok_service import TikTokService
from .services.instagram_service import InstagramService
from .database import get_db
from .core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Platform APIs Service",
    description="Service for uploading content to social media platforms",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8560"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
youtube_service = YouTubeService()
tiktok_service = TikTokService()
instagram_service = InstagramService()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "platform-apis", "timestamp": datetime.utcnow()}

@app.post("/api/platforms/upload", response_model=UploadResponse)
async def upload_content(
    request: UploadRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Upload content to specified platforms
    """
    try:
        # Create upload record
        upload_id = str(uuid.uuid4())
        
        # Start background upload process
        background_tasks.add_task(
            process_platform_uploads,
            upload_id,
            request,
            db
        )
        
        return UploadResponse(
            upload_id=upload_id,
            status="processing",
            message="Content upload started"
        )
        
    except Exception as e:
        logger.error(f"Error starting content upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start content upload")

@app.get("/api/platforms/status/{upload_id}", response_model=UploadStatus)
async def get_upload_status(upload_id: str, db = Depends(get_db)):
    """
    Get the current status of content uploads
    """
    try:
        # Query database for upload status
        # This would be implemented with actual database queries
        return UploadStatus(
            upload_id=upload_id,
            status="processing",
            platforms={
                "youtube": {"status": "uploading", "video_id": None, "url": None},
                "tiktok": {"status": "pending", "video_id": None, "url": None},
                "instagram": {"status": "pending", "video_id": None, "url": None}
            },
            error_message=None
        )
        
    except Exception as e:
        logger.error(f"Error getting upload status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get upload status")

@app.post("/api/platforms/schedule")
async def schedule_content(
    request: UploadRequest,
    schedule_time: datetime,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Schedule content upload for a specific time
    """
    try:
        # Create scheduled upload record
        upload_id = str(uuid.uuid4())
        
        # Schedule upload task
        background_tasks.add_task(
            schedule_platform_upload,
            upload_id,
            request,
            schedule_time,
            db
        )
        
        return {"message": f"Content scheduled for upload at {schedule_time}"}
        
    except Exception as e:
        logger.error(f"Error scheduling content upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to schedule content upload")

async def process_platform_uploads(upload_id: str, request: UploadRequest, db):
    """
    Background task for processing platform uploads
    """
    try:
        logger.info(f"Starting platform uploads for {upload_id}")
        
        results = {}
        
        # Upload to each platform
        for platform in request.platforms:
            try:
                if platform == "youtube":
                    result = await youtube_service.upload_video(
                        video_url=request.video_url,
                        title=request.title,
                        description=request.description,
                        tags=request.tags,
                        category_id=request.category_id
                    )
                    results["youtube"] = result
                    
                elif platform == "tiktok":
                    result = await tiktok_service.upload_video(
                        video_url=request.video_url,
                        caption=request.description,
                        privacy_level=request.privacy_level
                    )
                    results["tiktok"] = result
                    
                elif platform == "instagram":
                    result = await instagram_service.upload_reel(
                        video_url=request.video_url,
                        caption=request.description,
                        access_token=request.access_token
                    )
                    results["instagram"] = result
                    
            except Exception as e:
                logger.error(f"Error uploading to {platform}: {str(e)}")
                results[platform] = {"error": str(e)}
        
        # Update database with results
        logger.info(f"Platform uploads completed for {upload_id}")
        
    except Exception as e:
        logger.error(f"Error in platform uploads for {upload_id}: {str(e)}")

async def schedule_platform_upload(upload_id: str, request: UploadRequest, schedule_time: datetime, db):
    """
    Background task for scheduled uploads
    """
    try:
        logger.info(f"Scheduling upload for {upload_id} at {schedule_time}")
        
        # Calculate delay until schedule time
        delay = (schedule_time - datetime.utcnow()).total_seconds()
        
        if delay > 0:
            await asyncio.sleep(delay)
        
        # Process the upload
        await process_platform_uploads(upload_id, request, db)
        
    except Exception as e:
        logger.error(f"Error in scheduled upload for {upload_id}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8562)
