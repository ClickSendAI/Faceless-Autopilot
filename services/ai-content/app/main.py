"""
AI Content Generation Service
Handles script generation, voice synthesis, and video assembly
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import logging
from datetime import datetime
import uuid

from .schemas import ContentRequest, ContentResponse, ContentStatus
from .services.openai_service import OpenAIService
from .services.elevenlabs_service import ElevenLabsService
from .services.video_service import VideoService
from .database import get_db
from .core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Content Generation Service",
    description="Service for generating AI-powered content including scripts, voiceovers, and videos",
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
openai_service = OpenAIService()
elevenlabs_service = ElevenLabsService()
video_service = VideoService()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-content", "timestamp": datetime.utcnow()}

@app.post("/api/content/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Generate new AI content based on user requirements
    """
    try:
        # Create content record
        content_id = str(uuid.uuid4())
        
        # Start background generation process
        background_tasks.add_task(
            process_content_generation,
            content_id,
            request,
            db
        )
        
        return ContentResponse(
            content_id=content_id,
            status="processing",
            message="Content generation started"
        )
        
    except Exception as e:
        logger.error(f"Error starting content generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start content generation")

@app.get("/api/content/{content_id}/status", response_model=ContentStatus)
async def get_content_status(content_id: str, db = Depends(get_db)):
    """
    Get the current status of content generation
    """
    try:
        # Query database for content status
        # This would be implemented with actual database queries
        return ContentStatus(
            content_id=content_id,
            status="processing",
            progress=75,
            video_url=None,
            error_message=None
        )
        
    except Exception as e:
        logger.error(f"Error getting content status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get content status")

@app.post("/api/content/{content_id}/regenerate")
async def regenerate_content(
    content_id: str,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Regenerate content with updated parameters
    """
    try:
        # Start regeneration process
        background_tasks.add_task(
            process_content_regeneration,
            content_id,
            db
        )
        
        return {"message": "Content regeneration started"}
        
    except Exception as e:
        logger.error(f"Error starting content regeneration: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start content regeneration")

async def process_content_generation(content_id: str, request: ContentRequest, db):
    """
    Background task for content generation
    """
    try:
        logger.info(f"Starting content generation for {content_id}")
        
        # Step 1: Generate script using OpenAI
        script = await openai_service.generate_script(
            topic=request.topic,
            niche=request.niche,
            format=request.format,
            duration=request.duration
        )
        
        # Step 2: Generate voiceover using ElevenLabs
        voice_url = await elevenlabs_service.generate_voiceover(
            text=script,
            voice_id=request.voice_id
        )
        
        # Step 3: Assemble video using FFmpeg
        video_url = await video_service.assemble_video(
            script=script,
            voice_url=voice_url,
            format=request.format,
            platforms=request.platforms
        )
        
        # Update database with results
        # This would update the content record with final URLs
        
        logger.info(f"Content generation completed for {content_id}")
        
    except Exception as e:
        logger.error(f"Error in content generation for {content_id}: {str(e)}")
        # Update database with error status

async def process_content_regeneration(content_id: str, db):
    """
    Background task for content regeneration
    """
    try:
        logger.info(f"Starting content regeneration for {content_id}")
        # Implementation for regeneration logic
        logger.info(f"Content regeneration completed for {content_id}")
        
    except Exception as e:
        logger.error(f"Error in content regeneration for {content_id}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8561)
