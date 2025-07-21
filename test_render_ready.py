#!/usr/bin/env python3
"""
Test script to verify ChatApp is ready for Render deployment
Checks all production configurations and dependencies
"""

import os
import sys
import importlib.util
import json
from pathlib import Path

def test_render_readiness():
    """Test if the application is ready for Render deployment"""
    print("🔍 Testing Render Deployment Readiness")
    print("=" * 50)
    
    passed_tests = 0
    total_tests = 0
    
    # Test 1: Required Files
    print("\n1️⃣ Checking Required Files...")
    required_files = [
        'app.py',
        'requirements.txt', 
        'Procfile',
        'runtime.txt',
        'render.yaml',
        'database_config.py',
        '.env.example'
    ]
    
    for file in required_files:
        total_tests += 1
        if os.path.exists(file):
            print(f"✅ {file}")
            passed_tests += 1
        else:
            print(f"❌ {file} - Missing!")
    
    # Test 2: Directory Structure
    print("\n2️⃣ Checking Directory Structure...")
    required_dirs = [
        'static',
        'templates',
        'static/uploads',
        'static/profiles',
        'static/emotion_captures'
    ]
    
    for dir_path in required_dirs:
        total_tests += 1
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
            passed_tests += 1
        else:
            print(f"❌ {dir_path}/ - Missing!")
    
    # Test 3: Critical Imports
    print("\n3️⃣ Testing Critical Imports...")
    critical_imports = [
        ('flask', 'Flask'),
        ('flask_socketio', 'Flask-SocketIO'),
        ('bcrypt', 'Password Hashing'),
        ('cv2', 'OpenCV'),
        ('database_config', 'Database Configuration')
    ]
    
    for module, description in critical_imports:
        total_tests += 1
        try:
            __import__(module)
            print(f"✅ {description}")
            passed_tests += 1
        except ImportError as e:
            print(f"❌ {description} - {e}")
    
    # Test 4: Production Dependencies
    print("\n4️⃣ Checking Production Dependencies...")
    prod_deps = [
        ('gunicorn', 'WSGI Server'),
        ('psycopg2', 'PostgreSQL Driver (optional)')
    ]
    
    for module, description in prod_deps:
        total_tests += 1
        try:
            __import__(module)
            print(f"✅ {description}")
            passed_tests += 1
        except ImportError as e:
            if module == 'psycopg2':
                try:
                    import psycopg2
                    print(f"✅ {description}")
                    passed_tests += 1
                except ImportError:
                    print(f"⚠️  {description} - Will be installed on Render")
                    passed_tests += 1  # Not critical for local testing
            else:
                print(f"❌ {description} - {e}")
    
    # Test 5: Configuration Files Content
    print("\n5️⃣ Validating Configuration Files...")
    
    # Check Procfile
    total_tests += 1
    try:
        with open('Procfile', 'r') as f:
            procfile_content = f.read()
            if 'gunicorn' in procfile_content and 'app:app' in procfile_content:
                print("✅ Procfile - Valid")
                passed_tests += 1
            else:
                print("❌ Procfile - Invalid content")
    except Exception as e:
        print(f"❌ Procfile - Error reading: {e}")
    
    # Check runtime.txt
    total_tests += 1
    try:
        with open('runtime.txt', 'r') as f:
            runtime_content = f.read().strip()
            if runtime_content.startswith('python-'):
                print("✅ runtime.txt - Valid Python version")
                passed_tests += 1
            else:
                print("❌ runtime.txt - Invalid format")
    except Exception as e:
        print(f"❌ runtime.txt - Error reading: {e}")
    
    # Check requirements.txt
    total_tests += 1
    try:
        with open('requirements.txt', 'r') as f:
            req_content = f.read()
            required_packages = ['Flask', 'gunicorn', 'psycopg2-binary']
            missing_packages = []
            for pkg in required_packages:
                if pkg.lower() not in req_content.lower():
                    missing_packages.append(pkg)
            
            if not missing_packages:
                print("✅ requirements.txt - All essential packages present")
                passed_tests += 1
            else:
                print(f"❌ requirements.txt - Missing: {', '.join(missing_packages)}")
    except Exception as e:
        print(f"❌ requirements.txt - Error reading: {e}")
    
    # Test 6: App Configuration
    print("\n6️⃣ Checking App Configuration...")
    
    total_tests += 1
    try:
        # Check if app uses environment variables
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
            if 'os.environ.get' in app_content:
                print("✅ App uses environment variables")
                passed_tests += 1
            else:
                print("❌ App doesn't use environment variables")
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
    
    # Test 7: Database Configuration
    print("\n7️⃣ Testing Database Configuration...")
    
    total_tests += 1
    try:
        from database_config import get_db_connection, init_database
        print("✅ Database configuration module works")
        passed_tests += 1
    except Exception as e:
        print(f"❌ Database configuration error: {e}")
    
    # Test 8: Environment Variables Template
    print("\n8️⃣ Checking Environment Template...")
    
    total_tests += 1
    try:
        with open('.env.example', 'r') as f:
            env_content = f.read()
            required_vars = ['SECRET_KEY', 'DATABASE_URL', 'FLASK_ENV']
            missing_vars = []
            for var in required_vars:
                if var not in env_content:
                    missing_vars.append(var)
            
            if not missing_vars:
                print("✅ .env.example contains all required variables")
                passed_tests += 1
            else:
                print(f"❌ .env.example missing: {', '.join(missing_vars)}")
    except Exception as e:
        print(f"❌ .env.example error: {e}")
    
    # Test 9: Git Ignore Check
    print("\n9️⃣ Checking Git Configuration...")
    
    total_tests += 1
    try:
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content and '*.db' in gitignore_content:
                print("✅ .gitignore properly configured")
                passed_tests += 1
            else:
                print("❌ .gitignore missing important entries")
    except Exception as e:
        print(f"❌ .gitignore error: {e}")
    
    # Test 10: Health Check Endpoint
    print("\n🔟 Testing Health Check...")
    
    total_tests += 1
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
            if '/health' in app_content and 'health_check' in app_content:
                print("✅ Health check endpoint present")
                passed_tests += 1
            else:
                print("❌ Health check endpoint missing")
    except Exception as e:
        print(f"❌ Health check test error: {e}")
    
    # Results Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT! Your app is ready for Render deployment!")
        print("\n🚀 Next Steps:")
        print("1. Push your code to GitHub")
        print("2. Connect to Render and deploy")
        print("3. Add environment variables in Render dashboard")
        return True
    elif success_rate >= 75:
        print("⚠️  GOOD! Minor issues to fix before deployment.")
        print("\n🔧 Fix the failed tests above, then redeploy.")
        return False
    else:
        print("❌ NEEDS WORK! Several issues must be fixed.")
        print("\n🛠️  Address the failed tests before attempting deployment.")
        return False

def show_deployment_checklist():
    """Show the final deployment checklist"""
    print("\n" + "=" * 50)
    print("📋 RENDER DEPLOYMENT CHECKLIST")
    print("=" * 50)
    
    checklist = [
        "✅ Code pushed to GitHub",
        "✅ Render account created", 
        "✅ Web service connected to repository",
        "✅ Build command set: pip install -r requirements.txt",
        "✅ Start command set: gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app",
        "✅ Environment variables configured:",
        "   • SECRET_KEY (auto-generated)",
        "   • FLASK_ENV=production", 
        "   • DATABASE_URL (from PostgreSQL service)",
        "✅ PostgreSQL database created (optional)",
        "✅ First deployment triggered",
        "✅ Health check endpoint working: /health",
        "✅ All features tested on live URL"
    ]
    
    for item in checklist:
        print(item)
    
    print("\n🌐 Your app will be available at:")
    print("https://your-app-name.onrender.com")

if __name__ == "__main__":
    ready = test_render_readiness()
    
    if ready:
        show_deployment_checklist()
    
    print(f"\n📖 For detailed deployment guide, see: RENDER_DEPLOYMENT_GUIDE.md")
    
    sys.exit(0 if ready else 1)