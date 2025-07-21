# 🚀 ChatApp Installation Guide

Complete step-by-step guide to install and run ChatApp with all AI features.

## 📋 Prerequisites

Before installing ChatApp, ensure you have:

- **Python 3.8+** installed on your system
- **Git** for cloning the repository
- **Webcam** for AI features (emotion detection & mood filters)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

## 🛠️ Installation Methods

### Method 1: Automatic Setup (Recommended)

#### For Windows:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/tusharmishra57/ChatApp.git
   cd ChatApp
   ```

2. **Run the setup script:**
   ```bash
   setup.bat
   ```

3. **Start the application:**
   ```bash
   chatapp-env\Scripts\activate.bat
   python app.py
   ```

#### For Linux/macOS:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/tusharmishra57/ChatApp.git
   cd ChatApp
   ```

2. **Make setup script executable and run:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the application:**
   ```bash
   source chatapp-env/bin/activate
   python app.py
   ```

### Method 2: Manual Installation

#### Step 1: Clone Repository
```bash
git clone https://github.com/tusharmishra57/ChatApp.git
cd ChatApp
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv chatapp-env
chatapp-env\Scripts\activate

# Linux/macOS
python3 -m venv chatapp-env
source chatapp-env/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Create Required Directories
```bash
# Windows
mkdir static\uploads static\profiles static\emotion_captures static\anime_captures

# Linux/macOS
mkdir -p static/{uploads,profiles,emotion_captures,anime_captures}
```

#### Step 5: Test Installation
```bash
python test_mood_filter.py
python test_ai_features.py
```

#### Step 6: Run Application
```bash
python app.py
```

## 🌐 Access the Application

Once the server is running, open your browser and navigate to:
**http://localhost:5000**

## 🧪 Testing AI Features

### Test Emotion Detection
```bash
python emotion_detector.py
```

### Test Mood Filters
```bash
python anime_mood_filter.py
```

### Test Complete System
```bash
python test_ai_features.py
```

## 🚨 Troubleshooting

### Common Installation Issues

#### 1. Python Not Found
```bash
# Make sure Python is in your PATH
python --version
# or
python3 --version
```

#### 2. Permission Denied (Linux/macOS)
```bash
sudo pip install -r requirements.txt
# or use virtual environment (recommended)
```

#### 3. Visual C++ Build Tools (Windows)
If you encounter build errors:
1. Install Visual Studio Build Tools
2. Or install pre-compiled packages:
   ```bash
   pip install --only-binary=all opencv-python tensorflow
   ```

#### 4. Camera Access Issues
- **Chrome/Edge:** Allow camera permissions when prompted
- **Firefox:** Go to Settings > Privacy & Security > Permissions
- **Safari:** System Preferences > Security & Privacy > Camera

#### 5. TensorFlow/DeepFace Issues
```bash
# For CPU-only installation:
pip uninstall tensorflow tensorflow-gpu
pip install tensorflow==2.13.0

# For DeepFace issues:
pip install deepface==0.0.93
```

#### 6. Port Already in Use
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Linux/macOS - Kill process
lsof -ti:5000 | xargs kill -9

# Or use different port
export PORT=3000
python app.py
```

### Dependency Issues

#### Missing OpenCV
```bash
pip install opencv-python==4.8.1.78
```

#### Missing PIL/Pillow
```bash
pip install Pillow==10.0.1
```

#### Missing NumPy
```bash
pip install numpy==1.24.3
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
PORT=5000
DATABASE_URL=sqlite:///chat_app.db
```

### Camera Settings
Default camera settings (automatically configured):
- **Resolution:** 1280x720
- **FPS:** 30
- **Auto-focus:** Enabled

### AI Model Settings
Emotion detection uses DeepFace with these models:
- **Emotion Model:** Default DeepFace emotion model
- **Face Detection:** OpenCV Haar Cascades
- **Backup:** Random emotion for demo (if DeepFace fails)

## 🔧 Advanced Configuration

### Custom Anime Filter Styles
Edit `anime_mood_filter.py` to add custom styles:
```python
self.style_configs['YourStyle'] = {
    'name': 'Your Custom Style',
    'description': 'Your style description',
    'color_temp': 1.0,
    'saturation': 1.2,
    'edge_strength': 0.15
}
```

### Database Configuration
The app uses SQLite by default. For production, consider PostgreSQL:
```python
# In app.py
DATABASE_URL = 'postgresql://user:pass@localhost/chatapp'
```

### Performance Optimization
For better performance:
1. **Close unnecessary applications**
2. **Ensure good lighting** for camera
3. **Use Chrome** for best WebRTC support
4. **Update graphics drivers**

## 📊 System Requirements

### Minimum Requirements
- **OS:** Windows 10, macOS 10.14, or Linux Ubuntu 18.04+
- **Python:** 3.8+
- **RAM:** 4GB
- **Storage:** 2GB free space
- **Camera:** Any USB or built-in webcam

### Recommended Requirements
- **OS:** Windows 11, macOS 12+, or Linux Ubuntu 20.04+
- **Python:** 3.9+
- **RAM:** 8GB
- **Storage:** 5GB free space
- **Camera:** HD webcam (720p+)

## 🎯 Feature Testing

### 1. Basic Chat
- Register a new account
- Login and access dashboard
- Send messages to other users
- Check message history

### 2. Emotion Detection
- Click "Detect Emotion" button
- Allow camera access
- Position face in camera view
- Press SPACE to capture
- Send emotion to friends

### 3. Mood Filters
- Select anime style (Hayao, Shinkai, Paprika)
- Click "Apply MOOD Filter"
- Capture image
- Share filtered image with friends

### 4. Profile Management
- Upload profile picture
- Update user information
- View activity history

## 🔍 Verification Steps

After installation, verify everything works:

1. **Run test scripts:**
   ```bash
   python test_mood_filter.py
   python test_ai_features.py
   ```

2. **Check directories:**
   - `static/uploads/` exists
   - `static/profiles/` exists
   - `static/emotion_captures/` exists
   - `static/anime_captures/` exists

3. **Test web interface:**
   - Navigate to http://localhost:5000
   - Register a new account
   - Test all AI features
   - Check console for errors

## 📞 Support

If you encounter issues:

1. **Check this troubleshooting guide**
2. **Run test scripts** to identify problems
3. **Check GitHub issues** for similar problems
4. **Create a new issue** with error details

### Useful Commands for Debugging

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check virtual environment
echo $VIRTUAL_ENV  # Linux/macOS
echo %VIRTUAL_ENV% # Windows

# Test camera access
python -c "import cv2; print('Camera test:', cv2.VideoCapture(0).isOpened())"

# Test AI imports
python -c "from emotion_detector import EmotionDetector; print('Emotion detector OK')"
python -c "from anime_mood_filter import AnimeMoodFilter; print('Mood filter OK')"
```

## 🎉 Success!

If everything is working correctly, you should see:
- Web server running on port 5000
- No error messages in console
- Camera access granted in browser
- All AI features functional

**Enjoy your AI-powered chat application!** 🚀✨

---

For more help, visit: https://github.com/tusharmishra57/ChatApp/issues