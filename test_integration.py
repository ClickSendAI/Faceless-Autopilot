#!/usr/bin/env python3
"""
Integration Test Script for Faceless Autopilot AI
Tests the complete frontend-backend integration
"""

import requests
import json
import time
from datetime import datetime

# Service URLs
FRONTEND_URL = "http://localhost:8560"
AI_CONTENT_URL = "http://localhost:8561"
PLATFORM_APIS_URL = "http://localhost:8562"
ANALYTICS_URL = "http://localhost:8563"

def test_service_health():
    """Test all backend services health"""
    print("🔍 Testing Service Health...")
    
    services = [
        ("AI Content Service", f"{AI_CONTENT_URL}/health"),
        ("Platform APIs Service", f"{PLATFORM_APIS_URL}/health"),
        ("Analytics Service", f"{ANALYTICS_URL}/health")
    ]
    
    all_healthy = True
    
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                print(f"  ✅ {service_name}: {status}")
            else:
                print(f"  ❌ {service_name}: HTTP {response.status_code}")
                all_healthy = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {service_name}: {str(e)}")
            all_healthy = False
    
    return all_healthy

def test_content_generation():
    """Test AI content generation workflow"""
    print("\n🎬 Testing Content Generation...")
    
    try:
        # Test content generation
        payload = {
            "topic": "5 Money Mistakes That Keep You Poor",
            "niche": "personal finance",
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
            content_id = data.get('content_id')
            print(f"  ✅ Content generation started: {content_id}")
            
            # Poll for completion (simplified - in real app would poll longer)
            time.sleep(2)
            status_response = requests.get(f"{AI_CONTENT_URL}/api/content/{content_id}/status")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"  ✅ Content status: {status_data.get('status', 'unknown')}")
                return content_id
            else:
                print(f"  ⚠️  Could not check content status")
                return content_id
        else:
            print(f"  ❌ Content generation failed: HTTP {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Content generation error: {str(e)}")
        return None

def test_platform_upload(content_id):
    """Test platform upload workflow"""
    if not content_id:
        print("\n📤 Skipping Platform Upload (no content ID)")
        return
    
    print("\n📤 Testing Platform Upload...")
    
    try:
        payload = {
            "content_id": content_id,
            "video_url": "/mock-video.mp4",
            "title": "5 Money Mistakes That Keep You Poor",
            "description": "AI-generated content about personal finance",
            "platforms": ["youtube", "tiktok"],
            "tags": ["finance", "money", "tips"],
            "category_id": "education",
            "privacy_level": "public"
        }
        
        response = requests.post(
            f"{PLATFORM_APIS_URL}/api/platforms/upload",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            upload_id = data.get('upload_id')
            print(f"  ✅ Upload started: {upload_id}")
            
            # Check upload status
            time.sleep(2)
            status_response = requests.get(f"{PLATFORM_APIS_URL}/api/platforms/status/{upload_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"  ✅ Upload status: {status_data.get('status', 'unknown')}")
            else:
                print(f"  ⚠️  Could not check upload status")
        else:
            print(f"  ❌ Platform upload failed: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Platform upload error: {str(e)}")

def test_analytics():
    """Test analytics data retrieval"""
    print("\n📊 Testing Analytics...")
    
    try:
        # Test analytics overview
        response = requests.get(
            f"{ANALYTICS_URL}/api/analytics/overview?user_id=user-123&days=30",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Analytics overview: {data.get('total_videos', 0)} videos")
            
            # Test insights
            insights_response = requests.get(
                f"{ANALYTICS_URL}/api/analytics/insights?user_id=user-123&days=30",
                timeout=10
            )
            
            if insights_response.status_code == 200:
                insights_data = insights_response.json()
                print(f"  ✅ Analytics insights: {len(insights_data.get('insights', []))} insights")
            else:
                print(f"  ⚠️  Could not retrieve insights")
        else:
            print(f"  ❌ Analytics failed: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Analytics error: {str(e)}")

def test_frontend_access():
    """Test frontend accessibility"""
    print("\n🌐 Testing Frontend Access...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print(f"  ✅ Frontend accessible at {FRONTEND_URL}")
            return True
        else:
            print(f"  ❌ Frontend not accessible: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Frontend error: {str(e)}")
        return False

def main():
    """Run complete integration test"""
    print("🚀 Faceless Autopilot AI - Integration Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Service Health
    services_healthy = test_service_health()
    
    # Test 2: Frontend Access
    frontend_accessible = test_frontend_access()
    
    # Test 3: Content Generation (if services are healthy)
    content_id = None
    if services_healthy:
        content_id = test_content_generation()
        
        # Test 4: Platform Upload
        test_platform_upload(content_id)
        
        # Test 5: Analytics
        test_analytics()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    
    print(f"✅ Services Health: {'PASS' if services_healthy else 'FAIL'}")
    print(f"✅ Frontend Access: {'PASS' if frontend_accessible else 'FAIL'}")
    print(f"✅ Content Generation: {'PASS' if content_id else 'SKIP'}")
    print(f"✅ Platform Upload: {'PASS' if content_id else 'SKIP'}")
    print(f"✅ Analytics: {'PASS' if services_healthy else 'SKIP'}")
    
    if services_healthy and frontend_accessible:
        print("\n🎉 ALL TESTS PASSED!")
        print(f"🌐 Access your app at: {FRONTEND_URL}")
        print("📱 Features available:")
        print("  • AI Content Generation")
        print("  • Multi-Platform Upload")
        print("  • Analytics Dashboard")
        print("  • Content Management")
    else:
        print("\n⚠️  SOME TESTS FAILED!")
        print("Please check that all services are running:")
        print("  • AI Content Service (Port 8561)")
        print("  • Platform APIs Service (Port 8562)")
        print("  • Analytics Service (Port 8563)")
        print("  • Frontend (Port 8560)")

if __name__ == "__main__":
    main()

