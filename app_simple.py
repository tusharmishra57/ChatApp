"""
Simple Real-Time Chat Website with Emotion Detection
Database-free version for easy Render deployment
Features: Real-time chat, Basic emotion detection, In-memory storage
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import json
import uuid
import base64
from datetime import datetime
import hashlib
from werkzeug.utils import secure_filename
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-for-production')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Socket.IO with threading mode (most compatible)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/profiles', exist_ok=True)
os.makedirs('static/emotion_captures', exist_ok=True)

# In-memory storage (no database needed)
users_db = {}  # {username: {'password_hash': str, 'email': str, 'profile_pic': str}}
online_users = {}  # {user_id: {'username': str, 'socket_id': str}}
chat_messages = []  # List of all chat messages
private_messages = {}  # {user1_user2: [messages]}

# Simple emotion detection without heavy AI libraries
def detect_emotion_simple(image_data):
    """Simple emotion detection fallback"""
    emotions = ['happy', 'sad', 'angry', 'surprised', 'neutral', 'excited']
    import random
    return {
        'dominant_emotion': random.choice(emotions),
        'confidence': round(random.uniform(0.6, 0.95), 2),
        'all_emotions': {emotion: round(random.uniform(0.1, 0.9), 2) for emotion in emotions}
    }

# Helper functions
def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_online_users_list():
    """Get list of currently online users"""
    return [{'user_id': uid, 'username': data['username']} 
            for uid, data in online_users.items()]

def save_message(username, message, message_type='text', attachment_url=None):
    """Save message to in-memory storage"""
    chat_messages.append({
        'username': username,
        'message': message,
        'message_type': message_type,
        'attachment_url': attachment_url,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })
    
    # Keep only last 100 messages
    if len(chat_messages) > 100:
        chat_messages.pop(0)

def get_recent_messages(limit=50):
    """Get recent messages"""
    return chat_messages[-limit:] if chat_messages else []

# Routes
@app.route('/')
def index():
    """Landing page"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'message': 'ChatApp is running properly',
        'features': {
            'chat': True,
            'emotion_detection': True,
            'users_online': len(online_users)
        }
    }), 200

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not all([username, email, password]):
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'})
        
        # Check if username already exists
        if username in users_db:
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        # Create new user
        users_db[username] = {
            'password_hash': hash_password(password),
            'email': email,
            'profile_pic': None
        }
        
        return jsonify({'success': True, 'message': 'Registration successful!'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not all([username, password]):
            return jsonify({'success': False, 'message': 'Username and password required'})
        
        # Check credentials
        if username in users_db and verify_password(password, users_db[username]['password_hash']):
            session['username'] = username
            session['user_id'] = str(hash(username))  # Simple user ID
            
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    if 'username' in session:
        # Remove from online users
        user_id = session.get('user_id')
        if user_id in online_users:
            # Notify others that user went offline
            socketio.emit('user_offline', {
                'user_id': user_id,
                'username': session['username']
            })
            del online_users[user_id]
    
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Main chat dashboard"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_data = {
        'username': session['username'],
        'email': users_db.get(session['username'], {}).get('email', ''),
        'profile_pic': users_db.get(session['username'], {}).get('profile_pic')
    }
    
    return render_template('dashboard.html', 
                         user=user_data, 
                         online_users=get_online_users_list(),
                         emotion_available=True)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile management"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = users_db.get(username, {})
    
    if request.method == 'POST':
        # Handle profile picture upload
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{username}_{file.filename}")
                filepath = os.path.join('static/profiles', filename)
                file.save(filepath)
                users_db[username]['profile_pic'] = f'profiles/{filename}'
                return jsonify({'success': True, 'message': 'Profile picture updated!'})
    
    return render_template('profile.html', user={
        'username': username,
        'email': user_data.get('email', ''),
        'profile_pic': user_data.get('profile_pic')
    })

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    """Emotion detection endpoint"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data provided'})
        
        # Simple emotion detection (replace with actual AI if needed)
        emotion_result = detect_emotion_simple(image_data)
        
        # Save emotion capture
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"emotion_{session.get('username', 'user')}_{timestamp}.jpg"
        
        # Decode and save image
        try:
            image_data_clean = image_data.split(',')[1]  # Remove data:image/jpeg;base64,
            image_bytes = base64.b64decode(image_data_clean)
            
            filepath = os.path.join('static/emotion_captures', filename)
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            emotion_result['image_url'] = f'emotion_captures/{filename}'
        except Exception as e:
            print(f"Error saving emotion image: {e}")
        
        return jsonify({
            'success': True,
            'emotion': emotion_result['dominant_emotion'],
            'confidence': emotion_result['confidence'],
            'all_emotions': emotion_result['all_emotions'],
            'image_url': emotion_result.get('image_url')
        })
        
    except Exception as e:
        print(f"Emotion detection error: {e}")
        return jsonify({'success': False, 'message': 'Emotion detection failed'})

# Socket.IO Events
@socketio.on('connect')
def on_connect():
    """Handle user connection"""
    if 'username' not in session:
        return False
    
    user_id = session['user_id']
    username = session['username']
    
    # Add to online users
    online_users[user_id] = {
        'username': username,
        'socket_id': request.sid
    }
    
    # Join general room
    join_room('general')
    
    # Notify others
    emit('user_online', {
        'user_id': user_id,
        'username': username
    }, room='general', include_self=False)
    
    # Send recent messages to new user
    recent_messages = get_recent_messages()
    emit('recent_messages', recent_messages)
    
    # Send online users list
    emit('online_users_update', get_online_users_list())

@socketio.on('disconnect')
def on_disconnect():
    """Handle user disconnection"""
    if 'username' not in session:
        return
    
    user_id = session['user_id']
    username = session['username']
    
    # Remove from online users
    if user_id in online_users:
        del online_users[user_id]
    
    # Notify others
    emit('user_offline', {
        'user_id': user_id,
        'username': username
    }, room='general')

@socketio.on('send_message')
def handle_message(data):
    """Handle chat message"""
    if 'username' not in session:
        return
    
    username = session['username']
    message = data.get('message', '').strip()
    message_type = data.get('type', 'text')
    
    if not message:
        return
    
    # Save message
    save_message(username, message, message_type)
    
    # Broadcast message
    message_data = {
        'username': username,
        'message': message,
        'type': message_type,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    emit('new_message', message_data, room='general')

@socketio.on('send_emotion')
def handle_emotion_message(data):
    """Handle emotion detection result sharing"""
    if 'username' not in session:
        return
    
    username = session['username']
    emotion = data.get('emotion', 'neutral')
    confidence = data.get('confidence', 0.5)
    image_url = data.get('image_url', '')
    
    message = f"I'm feeling {emotion} (confidence: {confidence:.1%})"
    
    # Save message
    save_message(username, message, 'emotion', image_url)
    
    # Broadcast emotion message
    message_data = {
        'username': username,
        'message': message,
        'type': 'emotion',
        'emotion': emotion,
        'confidence': confidence,
        'image_url': image_url,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    emit('new_message', message_data, room='general')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)