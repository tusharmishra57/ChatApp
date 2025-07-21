@echo off
REM ChatApp Setup Script for Windows
REM This script will install all dependencies and set up the chat application

echo 🚀 ChatApp Setup Script
echo =======================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv chatapp-env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call chatapp-env\Scripts\activate.bat

REM Upgrade pip
echo 📈 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo 📁 Creating directories...
if not exist "static\uploads" mkdir static\uploads
if not exist "static\profiles" mkdir static\profiles
if not exist "static\emotion_captures" mkdir static\emotion_captures
if not exist "static\anime_captures" mkdir static\anime_captures

REM Create .gitkeep files
echo. > static\uploads\.gitkeep
echo. > static\profiles\.gitkeep
echo. > static\emotion_captures\.gitkeep
echo. > static\anime_captures\.gitkeep

echo ✅ Setup completed successfully!
echo.
echo 🎯 To run the application:
echo    1. Activate the virtual environment:
echo       chatapp-env\Scripts\activate.bat
echo    2. Run the application:
echo       python app.py
echo.
echo 🌐 The application will be available at http://localhost:5000
pause