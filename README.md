# 🚀 ChatApp - Real-Time Chat with AI Features

A modern, real-time chat application built with Flask and Socket.IO, featuring advanced AI capabilities including emotion detection and anime-style image filters.

![ChatApp Banner](https://img.shields.io/badge/ChatApp-Real--Time%20Chat-blue?style=for-the-badge&logo=chat&logoColor=white)

## ✨ Features

### 💬 Core Chat Features
- **Real-time messaging** with Socket.IO
- **Private conversations** between users
- **Online user tracking** and status indicators
- **Message history** with persistent storage
- **Typing indicators** for enhanced UX
- **Responsive design** with modern UI/UX

### 🤖 AI-Powered Features
- **Emotion Detection**: Real-time facial emotion recognition using DeepFace
- **Anime MOOD Filters**: Transform photos with 3 different anime styles:
  - 🎨 **Hayao (Studio Ghibli)**: Warm, soft colors inspired by Miyazaki films
  - 🌟 **Shinkai**: Vibrant, saturated colors with dramatic lighting
  - 🎭 **Paprika**: Psychedelic, intense colors with surreal effects

### 👤 User Management
- **User registration and authentication**
- **Profile management** with avatar uploads
- **Secure session handling**
- **SQLite database** for data persistence

## 🛠️ Technology Stack

- **Backend**: Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap Icons
- **Database**: SQLite
- **AI/ML**: DeepFace, TensorFlow, OpenCV
- **Real-time**: Socket.IO
- **Image Processing**: PIL, NumPy

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam (for AI features)
- Modern web browser with WebRTC support

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/tusharmishra57/ChatApp.git
cd ChatApp
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv anime-env
anime-env\Scripts\activate

# macOS/Linux
python3 -m venv anime-env
source anime-env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Browser
Navigate to `http://localhost:5000`

## 📦 Installation Details

### Core Dependencies
The application will automatically install:
- Flask and Flask-SocketIO for web framework
- DeepFace and TensorFlow for emotion detection
- OpenCV for image processing
- SQLite for database (built-in with Python)

### AI Features Setup
The AI features (emotion detection and anime filters) will be automatically configured on first run. If you encounter any issues:

1. **For Windows users**: Ensure you have Visual C++ Build Tools installed
2. **For macOS users**: Ensure Xcode command line tools are installed
3. **For Linux users**: Ensure build-essential is installed

## 🎮 How to Use

### Getting Started
1. **Register** a new account or **login** with existing credentials
2. **Upload a profile picture** (optional)
3. **Start chatting** with other online users

### Using AI Features

#### 🎭 Emotion Detection
1. Click **"Detect Emotion"** in the AI Features panel
2. Allow camera access when prompted
3. Position your face in the camera view
4. Press **SPACE** to capture or wait for auto-capture
5. View your detected emotion and confidence score
6. **Send the result** to friends in chat!

#### 🎨 Anime MOOD Filters
1. Select your preferred **anime style**:
   - **Shinkai**: For vibrant, cinematic looks
   - **Hayao**: For warm, Studio Ghibli aesthetics  
   - **Paprika**: For psychedelic, surreal effects
2. Click **"Apply MOOD Filter"**
3. Allow camera access and pose for the camera
4. Wait for the AI to process your image
5. **Share your anime transformation** with friends!

## 🏗️ Project Structure

```
ChatApp/
├── app.py                      # Main Flask application
├── emotion_detector.py         # AI emotion detection module
├── anime_mood_filter.py        # AI anime filter module
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                 # Git ignore rules
├── templates/                  # HTML templates
│   ├── base.html              # Base template with styling
│   ├── dashboard.html         # Main chat interface
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   └── profile.html           # User profile page
├── static/                    # Static files
│   ├── default_avatar.png     # Default user avatar
│   ├── uploads/               # User uploaded files
│   ├── profiles/              # Profile pictures
│   ├── emotion_captures/      # Emotion detection results
│   └── anime_captures/        # Anime filter results
└── emotion_web/               # Legacy emotion detection (optional)
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for custom configuration:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///chat_app.db
```

### Database
The application uses SQLite by default. The database file (`chat_app.db`) will be created automatically on first run.

## 🚨 Troubleshooting

### Common Issues

#### Camera Access Issues
- **Chrome/Edge**: Ensure you're accessing via `http://localhost:5000` (not `127.0.0.1`)
- **Firefox**: Allow camera permissions when prompted
- **Safari**: Check Privacy & Security settings

#### AI Features Not Working
```bash
# Test AI features
python test_ai_features.py
```

#### Installation Issues
```bash
# For TensorFlow issues on Windows
pip install tensorflow==2.13.0

# For OpenCV issues
pip install opencv-python==4.8.1.78

# For DeepFace issues
pip install deepface==0.0.93
```

#### Port Already in Use
```bash
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Kill process on port 5000 (macOS/Linux)
lsof -ti:5000 | xargs kill -9
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **DeepFace** for emotion recognition capabilities
- **TensorFlow** for machine learning framework
- **OpenCV** for computer vision processing
- **Flask-SocketIO** for real-time communication
- **Bootstrap Icons** for beautiful UI icons

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Run the test script: `python test_ai_features.py`
3. Open an issue on GitHub
4. Contact: [Your Email/Contact Info]

## 🌟 Star This Repository

If you found this project helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ by [Tushar Mishra](https://github.com/tusharmishra57)**

*Bringing AI-powered conversations to life!* 🚀✨
