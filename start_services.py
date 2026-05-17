#!/usr/bin/env python3
"""
Startup script for Faceless Autopilot AI services
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check if Python is available
    if not run_command("python --version"):
        print("❌ Python is not installed or not in PATH")
        return False
    
    # Check if pip is available
    if not run_command("pip --version"):
        print("❌ pip is not installed or not in PATH")
        return False
    
    print("✅ Dependencies check passed")
    return True

def install_requirements():
    """Install Python requirements for all services"""
    print("📦 Installing requirements...")
    
    services = ["ai-content", "platform-apis", "analytics"]
    
    for service in services:
        service_path = Path(f"services/{service}")
        requirements_file = service_path / "requirements.txt"
        
        if requirements_file.exists():
            print(f"Installing requirements for {service}...")
            result = run_command(f"pip install -r {requirements_file}", cwd=service_path)
            if result is None:
                print(f"❌ Failed to install requirements for {service}")
                return False
            print(f"✅ Requirements installed for {service}")
        else:
            print(f"⚠️  No requirements.txt found for {service}")
    
    return True

def start_services():
    """Start all services"""
    print("🚀 Starting services...")
    
    # Start AI Content Service
    print("Starting AI Content Service on port 8001...")
    ai_content_process = subprocess.Popen([
        "python", "-m", "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8001"
    ], cwd="services/ai-content")
    
    time.sleep(2)
    
    # Start Platform APIs Service
    print("Starting Platform APIs Service on port 8002...")
    platform_apis_process = subprocess.Popen([
        "python", "-m", "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8002"
    ], cwd="services/platform-apis")
    
    time.sleep(2)
    
    # Start Analytics Service
    print("Starting Analytics Service on port 8003...")
    analytics_process = subprocess.Popen([
        "python", "-m", "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8003"
    ], cwd="services/analytics")
    
    time.sleep(2)
    
    print("✅ All services started!")
    print("\n📋 Service URLs:")
    print("  - AI Content Service: http://localhost:8001")
    print("  - Platform APIs Service: http://localhost:8002")
    print("  - Analytics Service: http://localhost:8003")
    print("  - Frontend: http://localhost:4331")
    
    print("\n📚 API Documentation:")
    print("  - AI Content: http://localhost:8001/docs")
    print("  - Platform APIs: http://localhost:8002/docs")
    print("  - Analytics: http://localhost:8003/docs")
    
    print("\n🛑 Press Ctrl+C to stop all services")
    
    try:
        # Wait for user to stop services
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        ai_content_process.terminate()
        platform_apis_process.terminate()
        analytics_process.terminate()
        print("✅ All services stopped")

def main():
    """Main function"""
    print("🎬 Faceless Autopilot AI - Service Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("services").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Start services
    start_services()

if __name__ == "__main__":
    main()



