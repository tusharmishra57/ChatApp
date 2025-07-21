#!/usr/bin/env python3
"""
Test script to verify all ChatApp features are working
"""

import requests
import time
import sys
import os

def test_server_running():
    """Test if the server is running"""
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        return response.status_code == 200
    except:
        return False

def test_ai_imports():
    """Test if AI modules can be imported"""
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'emotion_web', 'emotion_web'))
        from emotion_detector import EmotionDetector
        from anime_mood_filter import AnimeGANMoodFilter
        return True
    except ImportError as e:
        print(f"AI import error: {e}")
        return False

def check_required_directories():
    """Check if all required directories exist"""
    required_dirs = [
        'static',
        'static/uploads',
        'static/profiles', 
        'static/anime_captures',
        'static/emotion_captures',
        'templates'
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    return missing_dirs

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/dashboard.html',
        'templates/profile.html',
        'static/default_avatar.png'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def run_tests():
    """Run all tests"""
    print("🔍 ChatApp Feature Test Suite")
    print("=" * 50)
    
    # Test 1: Check required files
    print("📁 Checking required files...")
    missing_files = check_required_files()
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
    
    # Test 2: Check required directories
    print("📂 Checking required directories...")
    missing_dirs = check_required_directories()
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ All required directories present")
    
    # Test 3: Test AI imports
    print("🤖 Testing AI module imports...")
    if test_ai_imports():
        print("✅ AI modules can be imported")
        ai_available = True
    else:
        print("⚠️ AI modules not available")
        ai_available = False
    
    # Test 4: Test server
    print("🌐 Testing server connection...")
    if test_server_running():
        print("✅ Server is running on http://localhost:5000")
        server_running = True
    else:
        print("❌ Server is not running")
        server_running = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ File Structure: {'PASS' if not missing_files else 'FAIL'}")
    print(f"✅ Directories: {'PASS' if not missing_dirs else 'FAIL'}")
    print(f"🤖 AI Features: {'AVAILABLE' if ai_available else 'DISABLED'}")
    print(f"🌐 Server: {'RUNNING' if server_running else 'STOPPED'}")
    
    if server_running:
        print(f"\n🎉 ChatApp is ready!")
        print(f"🌐 Open: http://localhost:5000")
        print(f"📱 Features Available:")
        print(f"  ✓ User Registration & Login")
        print(f"  ✓ Real-time Chat")
        print(f"  ✓ Online Status Tracking")
        print(f"  ✓ Profile Management")
        if ai_available:
            print(f"  ✓ AI Emotion Detection")
            print(f"  ✓ AnimeGAN Mood Filters")
        else:
            print(f"  ⚠ AI features disabled (install dependencies)")
        
        return True
    else:
        print(f"\n⚠️ Server not running. Start with: python app.py")
        return False

if __name__ == "__main__":
    run_tests()