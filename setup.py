"""
Setup script for ChatApp with AI Features
Run this script to set up the environment and install dependencies
"""

import os
import sys
import subprocess
import urllib.request
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚀 ChatApp with AI Features - Setup Script")
    print("=" * 60)
    print("This script will set up your chat application with:")
    print("✓ Real-time chat functionality")
    print("✓ User authentication system")
    print("✓ Emotion detection with AI")
    print("✓ AnimeGAN mood filters")
    print("✓ Beautiful dark-themed UI")
    print("=" * 60)

def check_python_version():
    """Check Python version compatibility"""
    print("📋 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible")
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directory structure...")
    
    directories = [
        "static",
        "static/uploads", 
        "static/profiles",
        "static/anime_captures",
        "static/emotion_captures",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

def download_default_avatar():
    """Download a default avatar image"""
    print("🖼️ Setting up default avatar...")
    
    avatar_url = "https://via.placeholder.com/150x150/64FFDA/000000?text=👤"
    avatar_path = "static/default_avatar.png"
    
    try:
        if not os.path.exists(avatar_path):
            print("📥 Downloading default avatar...")
            urllib.request.urlretrieve(avatar_url, avatar_path)
            print("✅ Default avatar downloaded")
        else:
            print("✅ Default avatar already exists")
    except Exception as e:
        print(f"⚠️ Could not download default avatar: {e}")
        print("You can manually add a default_avatar.png file in the static folder")

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python packages...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        print("Please install packages manually using: pip install -r requirements.txt")
        return False

def setup_emotion_detection():
    """Set up emotion detection components"""
    print("🤖 Setting up AI components...")
    
    # Check if emotion detection files exist
    emotion_path = Path("emotion_web/emotion_web")
    
    if emotion_path.exists():
        print("✅ Emotion detection files found")
        
        # Check for AnimeGAN model
        animegan_path = emotion_path / "AnimeGANv2"
        if animegan_path.exists():
            print("✅ AnimeGAN model found")
        else:
            print("⚠️ AnimeGAN model not found - mood filters may not work")
        
        return True
    else:
        print("⚠️ Emotion detection files not found")
        print("AI features will be disabled")
        return False

def create_run_script():
    """Create a convenient run script"""
    print("📜 Creating run script...")
    
    run_script = """#!/usr/bin/env python3
\"\"\"
Quick start script for ChatApp
\"\"\"

import os
import sys

if __name__ == "__main__":
    print("🚀 Starting ChatApp...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📝 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        os.system("python app.py")
    except KeyboardInterrupt:
        print("\\n👋 ChatApp stopped. Goodbye!")
"""
    
    with open("run.py", "w") as f:
        f.write(run_script)
    
    print("✅ Created run.py script")

def show_next_steps():
    """Show next steps to user"""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run the application:")
    print("   python app.py")
    print("   OR")
    print("   python run.py")
    print("\n2. Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n3. Create an account and start chatting!")
    print("\nFeatures available:")
    print("✓ Real-time chat")
    print("✓ User registration & login")
    print("✓ Online status tracking")
    print("✓ Profile customization")
    
    emotion_available = os.path.exists("emotion_web/emotion_web/emotion_detector.py")
    if emotion_available:
        print("✓ AI emotion detection")
        print("✓ AnimeGAN mood filters")
    else:
        print("⚠ AI features disabled (emotion detection files not found)")
    
    print("\n📚 For more information, check the README files in emotion_web/emotion_web/")
    print("=" * 60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Download default avatar
    download_default_avatar()
    
    # Install requirements
    if not install_requirements():
        print("⚠️ Package installation failed. Please install manually.")
    
    # Setup emotion detection
    setup_emotion_detection()
    
    # Create run script
    create_run_script()
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        input("\nPress Enter to continue...")