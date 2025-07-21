#!/bin/bash
# ChatApp Setup Script
# This script will install all dependencies and set up the chat application

echo "🚀 ChatApp Setup Script"
echo "======================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv chatapp-env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source chatapp-env/Scripts/activate
else
    source chatapp-env/bin/activate
fi

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p static/uploads
mkdir -p static/profiles
mkdir -p static/emotion_captures
mkdir -p static/anime_captures

# Create .gitkeep files
touch static/uploads/.gitkeep
touch static/profiles/.gitkeep
touch static/emotion_captures/.gitkeep
touch static/anime_captures/.gitkeep

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 To run the application:"
echo "   1. Activate the virtual environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "      source chatapp-env/Scripts/activate"
else
    echo "      source chatapp-env/bin/activate"
fi
echo "   2. Run the application:"
echo "      python app.py"
echo ""
echo "🌐 The application will be available at http://localhost:5000"