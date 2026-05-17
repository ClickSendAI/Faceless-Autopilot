#!/usr/bin/env python3
"""
Simple test script for Faceless Autopilot AI APIs
"""

import requests
import json
import time

# API endpoints
AI_CONTENT_URL = "http://localhost:8561"
PLATFORM_APIS_URL = "http://localhost:8562"
ANALYTICS_URL = "http://localhost:8563"

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
    print("\nTesting AI content generation...")
    
    try:
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
            print(f"OK Content generation started: {data.get('content_id', 'unknown')}")
            return data.get('content_id')
        else:
            print(f"ERROR Content generation failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR Content generation request failed: {e}")
        return None

def main():
    """Main test function"""
    print("Faceless Autopilot AI - API Testing")
    print("=" * 50)
    
    # Wait a moment for services to start
    print("Waiting for services to start...")
    time.sleep(3)
    
    # Test health endpoints
    test_health_endpoints()
    
    # Test AI content generation
    content_id = test_ai_content_generation()
    
    print("\nAPI testing completed!")
    print("\nAPI Documentation:")
    print(f"  - AI Content: {AI_CONTENT_URL}/docs")
    print(f"  - Platform APIs: {PLATFORM_APIS_URL}/docs")
    print(f"  - Analytics: {ANALYTICS_URL}/docs")

if __name__ == "__main__":
    main()
