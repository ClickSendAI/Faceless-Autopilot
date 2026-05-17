#!/usr/bin/env python3
"""
Test script for Faceless Autopilot AI APIs
"""

import requests
import json
import time
from datetime import datetime

# API endpoints
AI_CONTENT_URL = "http://localhost:8001"
PLATFORM_APIS_URL = "http://localhost:8002"
ANALYTICS_URL = "http://localhost:8003"

def test_health_endpoints():
    """Test health endpoints for all services"""
    print("Testing health endpoints...")
    
    services = [
        ("AI Content", f"{AI_CONTENT_URL}/health"),
        ("Platform APIs", f"{PLATFORM_APIS_URL}/health"),
        ("Analytics", f"{ANALYTICS_URL}/health")
    ]
    
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"OK {service_name}: {data.get('status', 'unknown')}")
            else:
                print(f"ERROR {service_name}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR {service_name}: Connection failed - {e}")

def test_ai_content_generation():
    """Test AI content generation API"""
    print("\n🤖 Testing AI content generation...")
    
    try:
        # Test content generation request
        payload = {
            "topic": "AI Productivity Tips",
            "niche": "productivity",
            "format": "short",
            "duration": 60,
            "voice_id": "default",
            "platforms": ["youtube", "tiktok"],
            "style": "educational",
            "tone": "professional"
        }
        
        response = requests.post(
            f"{AI_CONTENT_URL}/api/content/generate",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content generation started: {data.get('content_id', 'unknown')}")
            return data.get('content_id')
        else:
            print(f"❌ Content generation failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Content generation request failed: {e}")
        return None

def test_content_status(content_id):
    """Test content status API"""
    if not content_id:
        return
        
    print(f"\n📊 Testing content status for {content_id}...")
    
    try:
        response = requests.get(
            f"{AI_CONTENT_URL}/api/content/{content_id}/status",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content status: {data.get('status', 'unknown')}")
            print(f"   Progress: {data.get('progress', 0)}%")
        else:
            print(f"❌ Status check failed: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Status check request failed: {e}")

def test_platform_upload():
    """Test platform upload API"""
    print("\n📤 Testing platform upload...")
    
    try:
        payload = {
            "content_id": "test-content-123",
            "video_url": "https://example.com/video.mp4",
            "title": "Test Video",
            "description": "This is a test video",
            "platforms": ["youtube", "tiktok"],
            "tags": ["test", "ai", "automation"]
        }
        
        response = requests.post(
            f"{PLATFORM_APIS_URL}/api/platforms/upload",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Upload started: {data.get('upload_id', 'unknown')}")
            return data.get('upload_id')
        else:
            print(f"❌ Upload failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload request failed: {e}")
        return None

def test_analytics():
    """Test analytics API"""
    print("\n📈 Testing analytics...")
    
    try:
        # Test analytics overview
        response = requests.get(
            f"{ANALYTICS_URL}/api/analytics/overview?user_id=test-user&days=30",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analytics overview retrieved")
        else:
            print(f"❌ Analytics overview failed: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Analytics request failed: {e}")

def main():
    """Main test function"""
    print("Faceless Autopilot AI - API Testing")
    print("=" * 50)
    
    # Wait a moment for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(3)
    
    # Test health endpoints
    test_health_endpoints()
    
    # Test AI content generation
    content_id = test_ai_content_generation()
    
    # Test content status
    test_content_status(content_id)
    
    # Test platform upload
    upload_id = test_platform_upload()
    
    # Test analytics
    test_analytics()
    
    print("\n✅ API testing completed!")
    print("\n📚 API Documentation:")
    print(f"  - AI Content: {AI_CONTENT_URL}/docs")
    print(f"  - Platform APIs: {PLATFORM_APIS_URL}/docs")
    print(f"  - Analytics: {ANALYTICS_URL}/docs")

if __name__ == "__main__":
    main()
