"""
Pydantic models for Analytics Service
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalyticsOverview(BaseModel):
    """Analytics overview model"""
    total_videos: int = Field(..., description="Total videos generated")
    total_views: int = Field(..., description="Total views across all platforms")
    total_revenue: float = Field(..., description="Total revenue generated")
    engagement_rate: float = Field(..., description="Average engagement rate")
    top_performing_content: List[Dict[str, Any]] = Field(..., description="Top performing content")
    platform_breakdown: Dict[str, int] = Field(..., description="Views by platform")

class ContentAnalytics(BaseModel):
    """Content-specific analytics model"""
    content_id: str = Field(..., description="Content ID")
    title: str = Field(..., description="Content title")
    total_views: int = Field(..., description="Total views")
    engagement_rate: float = Field(..., description="Engagement rate")
    revenue: float = Field(..., description="Revenue generated")
    platform_analytics: Dict[str, Dict[str, Any]] = Field(..., description="Platform-specific analytics")
    created_at: datetime = Field(..., description="Content creation date")

class PerformanceInsights(BaseModel):
    """Performance insights model"""
    insights: List[str] = Field(..., description="Performance insights")
    recommendations: List[str] = Field(..., description="Optimization recommendations")
    trends: Dict[str, Any] = Field(..., description="Performance trends")
    best_posting_times: Dict[str, str] = Field(..., description="Best posting times by platform")



