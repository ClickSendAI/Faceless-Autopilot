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
from .database import get_db, SessionLocal
from .models import Content
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
        content_id = str(uuid.uuid4())

        # Persist initial record so status polling works immediately
        record = Content(
            id=content_id,
            user_id="00000000-0000-0000-0000-000000000000",
            title=request.topic,
            description=f"Auto-generated: {request.niche} / {request.format}",
            status="processing",
            platforms=request.platforms,
        )
        db.add(record)
        db.commit()

        # Start background generation process (uses its own session)
        background_tasks.add_task(
            process_content_generation,
            content_id,
            request,
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
        record = db.query(Content).filter(Content.id == content_id).first()
        if record is None:
            raise HTTPException(status_code=404, detail="Content not found")

        status_to_progress = {"processing": 50, "completed": 100, "failed": 0}
        progress = status_to_progress.get(record.status, 0)

        return ContentStatus(
            content_id=content_id,
            status=record.status,
            progress=progress,
            video_url=record.video_file_url,
            error_message=None
        )

    except HTTPException:
        raise
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
        )
        
        return {"message": "Content regeneration started"}
        
    except Exception as e:
        logger.error(f"Error starting content regeneration: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start content regeneration")

async def process_content_generation(content_id: str, request: ContentRequest):
    """
    Background task for content generation. Opens its own DB session.
    """
    db = SessionLocal()
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

        # Persist results
        record = db.query(Content).filter(Content.id == content_id).first()
        if record:
            record.script = script
            record.voice_file_url = voice_url
            record.video_file_url = video_url
            record.status = "completed"
            db.commit()

        logger.info(f"Content generation completed for {content_id}")

    except Exception as e:
        logger.error(f"Error in content generation for {content_id}: {str(e)}")
        record = db.query(Content).filter(Content.id == content_id).first()
        if record:
            record.status = "failed"
            db.commit()
    finally:
        db.close()

async def process_content_regeneration(content_id: str):
    """
    Background task for content regeneration. Opens its own DB session.
    """
    db = SessionLocal()
    try:
        logger.info(f"Starting content regeneration for {content_id}")

        record = db.query(Content).filter(Content.id == content_id).first()
        if record is None:
            logger.error(f"Content {content_id} not found for regeneration")
            return

        record.status = "processing"
        db.commit()

        # Re-generate script and media using existing topic/niche stored in description
        script = await openai_service.generate_script(
            topic=record.title,
            niche=record.description or "general",
            format="short",
            duration=60
        )
        voice_url = await elevenlabs_service.generate_voiceover(text=script)
        platforms = record.platforms or ["youtube"]
        video_url = await video_service.assemble_video(
            script=script,
            voice_url=voice_url,
            format="short",
            platforms=platforms
        )

        record.script = script
        record.voice_file_url = voice_url
        record.video_file_url = video_url
        record.status = "completed"
        db.commit()

        logger.info(f"Content regeneration completed for {content_id}")

    except Exception as e:
        logger.error(f"Error in content regeneration for {content_id}: {str(e)}")
        record = db.query(Content).filter(Content.id == content_id).first()
        if record:
            record.status = "failed"
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8561)
