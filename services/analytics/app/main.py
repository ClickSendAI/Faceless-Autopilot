"""
Analytics Service
Handles performance tracking, insights, and revenue analytics
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from .schemas import AnalyticsOverview, ContentAnalytics, PerformanceInsights
from .services.analytics_service import AnalyticsService
from .database import get_db
from .core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Analytics Service",
    description="Service for content performance analytics and insights",
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
analytics_service = AnalyticsService()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "analytics", "timestamp": datetime.utcnow()}

@app.get("/api/analytics/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    user_id: str,
    days: int = Query(default=30, description="Number of days to analyze"),
    db = Depends(get_db)
):
    """
    Get overall analytics overview for a user
    """
    try:
        overview = await analytics_service.get_user_overview(user_id, days, db)
        return overview
        
    except Exception as e:
        logger.error(f"Error getting analytics overview: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get analytics overview")

@app.get("/api/analytics/content/{content_id}", response_model=ContentAnalytics)
async def get_content_analytics(
    content_id: str,
    db = Depends(get_db)
):
    """
    Get detailed analytics for specific content
    """
    try:
        analytics = await analytics_service.get_content_analytics(content_id, db)
        return analytics
        
    except Exception as e:
        logger.error(f"Error getting content analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get content analytics")

@app.get("/api/analytics/insights", response_model=PerformanceInsights)
async def get_performance_insights(
    user_id: str,
    days: int = Query(default=30, description="Number of days to analyze"),
    db = Depends(get_db)
):
    """
    Get performance insights and recommendations
    """
    try:
        insights = await analytics_service.get_performance_insights(user_id, days, db)
        return insights
        
    except Exception as e:
        logger.error(f"Error getting performance insights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get performance insights")

@app.post("/api/analytics/sync")
async def sync_platform_analytics(
    user_id: str,
    platforms: List[str],
    db = Depends(get_db)
):
    """
    Sync analytics data from platforms
    """
    try:
        results = await analytics_service.sync_platform_data(user_id, platforms, db)
        return {"message": "Analytics sync completed", "results": results}
        
    except Exception as e:
        logger.error(f"Error syncing platform analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to sync platform analytics")

@app.get("/api/analytics/revenue")
async def get_revenue_analytics(
    user_id: str,
    days: int = Query(default=30, description="Number of days to analyze"),
    db = Depends(get_db)
):
    """
    Get revenue analytics and projections
    """
    try:
        revenue_data = await analytics_service.get_revenue_analytics(user_id, days, db)
        return revenue_data
        
    except Exception as e:
        logger.error(f"Error getting revenue analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get revenue analytics")

@app.get("/api/analytics/trends")
async def get_content_trends(
    user_id: str,
    niche: Optional[str] = None,
    days: int = Query(default=30, description="Number of days to analyze"),
    db = Depends(get_db)
):
    """
    Get content performance trends
    """
    try:
        trends = await analytics_service.get_content_trends(user_id, niche, days, db)
        return trends
        
    except Exception as e:
        logger.error(f"Error getting content trends: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get content trends")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8563)
