"""
Real-Time Chat Website with Emotion Detection and Mood Filters
Features: Real-time chat, Authentication, Online status, Emotion detection, AnimeGAN filters, Profile management
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
import os
import json
import uuid
import base64
import sqlite3
from datetime import datetime
import bcrypt
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import threading
import time
import sys
from database_config import get_db_connection_simple as get_db_connection, init_database

# AI Features - Render-optimized with graceful fallback
EMOTION_AVAILABLE = False
EMOTION_METHOD = None
emotion_detector = None

try:
    # Try FER first (lightweight for Render)
    from fer import FER
    emotion_detector = FER(mtcnn=True)
    EMOTION_AVAILABLE = True
    EMOTION_METHOD = 'FER'
    print("✓ FER emotion detection loaded!")
except ImportError:
    try:
        # Fallback to custom emotion detector
        from emotion_detector import EmotionDetector
        emotion_detector = EmotionDetector()
        EMOTION_AVAILABLE = True
        EMOTION_METHOD = 'CUSTOM'
        print("✓ Custom emotion detection loaded!")
    except ImportError:
        # Graceful fallback - app still works without AI
        print("⚠ Emotion detection not available - continuing without AI features")
        EMOTION_AVAILABLE = False
        EMOTION_METHOD = 'NONE'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-for-production')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database configuration for Render
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///chat_app.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
app.config['DATABASE_URL'] = DATABASE_URL

# Render environment detection
IS_RENDER = os.environ.get('RENDER') is not None

# Socket.IO with flexible async mode
try:
    # Try gevent first (for Render)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
    print("✓ Using gevent async mode")
except:
    try:
        # Fallback to eventlet
        socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
        print("✓ Using eventlet async mode")
    except:
        # Final fallback to threading
        socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
        print("✓ Using threading async mode")

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/profiles', exist_ok=True)
os.makedirs('static/emotion_captures', exist_ok=True)

# Global variables for tracking online users and chat rooms
online_users = {}  # {user_id: {'username': str, 'room': str, 'socket_id': str}}
chat_rooms = {'general': {'users': [], 'messages': []}}

# Initialize emotion detector if available
# AI systems will be initialized per request to avoid conflicts



# Helper functions


def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def update_user_online_status(user_id, is_online):
    """Update user's online status in database"""
    conn = get_db_connection()
    conn.execute('UPDATE users SET is_online = ?, last_login = ? WHERE id = ?',
                (int(is_online), datetime.now(), user_id))
    conn.commit()
    conn.close()

def get_online_users_list():
    """Get list of currently online users"""
    return [{'user_id': uid, 'username': data['username']} 
            for uid, data in online_users.items()]

def save_message_to_db(user_id, username, room, message, message_type='text', attachment_url=None):
    """Save message to database"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO messages (user_id, username, room, message, message_type, attachment_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, room, message, message_type, attachment_url))
    conn.commit()
    conn.close()

def get_recent_messages(room='general', limit=50):
    """Get recent messages from database"""
    conn = get_db_connection()
    messages = conn.execute('''
        SELECT username, message, message_type, attachment_url, timestamp
        FROM messages
        WHERE room = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (room, limit)).fetchall()
    conn.close()
    
    # Convert to list of dicts and reverse order
    return [dict(msg) for msg in reversed(messages)]

def save_private_message_to_db(user_id, username, recipient, message, message_type='text', extra_data=None):
    """Save private message to database"""
    try:
        conn = get_db_connection()
        
        # Create private_messages table if it doesn't exist
        conn.execute('''
            CREATE TABLE IF NOT EXISTS private_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                sender_username TEXT NOT NULL,
                recipient_username TEXT NOT NULL,
                message TEXT NOT NULL,
                message_type TEXT DEFAULT 'text',
                extra_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users (id)
            )
        ''')
        
        # Save extra data as JSON if provided
        extra_json = None
        if extra_data and message_type in ['emotion', 'mood_filter']:
            import json
            extra_json = json.dumps(extra_data)
        
        conn.execute('''
            INSERT INTO private_messages (sender_id, sender_username, recipient_username, message, message_type, extra_data, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, recipient, message, message_type, extra_json, datetime.now()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving private message: {e}")

def get_chat_history_from_db(user1, user2, limit=50):
    """Get chat history between two users"""
    try:
        conn = get_db_connection()
        
        # Get messages where user1 sent to user2 OR user2 sent to user1
        messages = conn.execute('''
            SELECT sender_username, recipient_username, message, message_type, extra_data, 
                   strftime('%H:%M:%S', timestamp) as time
            FROM private_messages 
            WHERE (sender_username = ? AND recipient_username = ?) 
               OR (sender_username = ? AND recipient_username = ?)
            ORDER BY timestamp ASC
            LIMIT ?
        ''', (user1, user2, user2, user1, limit)).fetchall()
        
        conn.close()
        
        # Format messages for frontend
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                'sender': msg['sender_username'],
                'recipient': msg['recipient_username'],
                'message': msg['message'],
                'type': msg['message_type'],
                'timestamp': msg['time'],
                'extra_data': msg['extra_data']
            })
        
        return formatted_messages
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return []

def get_user_socket(username):
    """Get socket ID for a user"""
    for user_id, user_data in online_users.items():
        if user_data['username'] == username:
            return user_data['socket_id']
    return None

# Authentication routes
@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        conn = get_db_connection()
        conn.close()
        return jsonify({
            'status': 'healthy',
            'message': 'ChatApp is running properly',
            'features': {
                'chat': True,
                'emotion_detection': EMOTION_AVAILABLE,
                'mood_filter': 'coming_soon'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Health check failed: {str(e)}'
        }), 500

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
        
        conn = get_db_connection()
        
        # Check if username or email already exists
        existing = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?',
                               (username, email)).fetchone()
        if existing:
            conn.close()
            return jsonify({'success': False, 'message': 'Username or email already exists'})
        
        # Create new user
        password_hash = hash_password(password)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Registration successful!'})
        except Exception as e:
            conn.close()
            return jsonify({'success': False, 'message': 'Registration failed'})
    
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
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?',
                           (username, username)).fetchone()
        conn.close()
        
        if user and verify_password(password, user['password_hash']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            # Update online status
            update_user_online_status(user['id'], True)
            
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    if 'user_id' in session:
        update_user_online_status(session['user_id'], False)
        
        # Remove from online users
        user_id = str(session['user_id'])
        if user_id in online_users:
            del online_users[user_id]
        
        # Notify others that user went offline
        socketio.emit('user_offline', {
            'user_id': user_id,
            'username': session['username']
        }, room='general')
    
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Main chat dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user info
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                       (session['user_id'],)).fetchone()
    conn.close()
    
    if not user:
        return redirect(url_for('logout'))
    
    return render_template('dashboard.html', 
                         user=dict(user), 
                         online_users=get_online_users_list(),
                         emotion_available=EMOTION_AVAILABLE)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile management"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                       (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        # Handle profile updates
        new_username = request.form.get('username', '').strip()
        
        if new_username and new_username != user['username']:
            # Check if username is available
            existing = conn.execute('SELECT id FROM users WHERE username = ? AND id != ?',
                                   (new_username, session['user_id'])).fetchone()
            if existing:
                flash('Username already taken', 'error')
            else:
                conn.execute('UPDATE users SET username = ? WHERE id = ?',
                           (new_username, session['user_id']))
                session['username'] = new_username
                flash('Username updated successfully!', 'success')
        
        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename and allowed_file(file.filename):
                filename = secure_filename(f"profile_{session['user_id']}_{file.filename}")
                filepath = os.path.join('static/profiles', filename)
                file.save(filepath)
                
                conn.execute('UPDATE users SET profile_picture = ? WHERE id = ?',
                           (filename, session['user_id']))
                flash('Profile picture updated successfully!', 'success')
        
        conn.commit()
    
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                       (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('profile.html', user=dict(user))

# Emotion Detection Routes
@app.route('/emotion_detect', methods=['POST'])
def emotion_detect():
    """Handle emotion detection request"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    if not EMOTION_AVAILABLE:
        return jsonify({'success': False, 'message': 'Emotion detection not available'})
    
    try:
        if EMOTION_METHOD == 'FER' and emotion_detector:
            # Use FER for emotion detection
            try:
                import cv2
                import numpy as np
                import base64
                from PIL import Image
                import io
                
                # Get image data from request
                data = request.get_json()
                if not data or 'image' not in data:
                    return jsonify({'success': False, 'message': 'No image provided'})
                
                # Decode base64 image
                image_data = data['image'].split(',')[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Detect emotion using FER
                emotions = emotion_detector.detect_emotions(image_cv)
                
                if emotions:
                    dominant_emotion = max(emotions[0]['emotions'].items(), key=lambda x: x[1])
                    emotion = dominant_emotion[0]
                    confidence = dominant_emotion[1] * 100
                    
                    result = {
                        'success': True,
                        'emotion': emotion,
                        'confidence': confidence,
                        'message': f'Detected {emotion} with {confidence:.1f}% confidence'
                    }
                else:
                    result = {'success': False, 'message': 'No face detected'}
            except Exception as fer_error:
                result = {'success': False, 'message': f'FER error: {str(fer_error)}'}
                
        elif EMOTION_METHOD == 'CUSTOM' and emotion_detector:
            # Use custom emotion detector
            result = emotion_detector.detect_emotion_from_camera()
        else:
            # Fallback when no emotion detection available
            result = {
                'success': False, 
                'message': 'Emotion detection is temporarily unavailable. Chat still works!'
            }
        
        if result.get('success'):
            emotion = result['emotion']
            confidence = result['confidence']
            
            # Save to database
            conn = get_db_connection()
            conn.execute('''
                CREATE TABLE IF NOT EXISTS emotion_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    emotion TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.execute('''
                INSERT INTO emotion_records (user_id, emotion, confidence)
                VALUES (?, ?, ?)
            ''', (session['user_id'], emotion, confidence))
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'emotion': emotion,
                'confidence': confidence,
                'message': result['message'],
                'emoji': result.get('emoji', '😐')
            })
        else:
            return jsonify({'success': False, 'message': result['message']})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/mood_filter', methods=['POST'])
def mood_filter_route():
    """Handle mood filter request - Coming Soon"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    return jsonify({
        'success': False, 
        'message': '🎨 MOOD Filter feature is coming soon! Stay tuned for amazing anime-style transformations.',
        'coming_soon': True
    })

# Socket.IO events for real-time chat
@socketio.on('connect')
def handle_connect():
    """Handle user connection"""
    if 'user_id' in session:
        user_id = str(session['user_id'])
        username = session['username']
        
        # Add to online users
        online_users[user_id] = {
            'username': username,
            'room': 'general',
            'socket_id': request.sid
        }
        
        # Join general room
        join_room('general')
        
        # Notify others
        emit('user_online', {
            'user_id': user_id,
            'username': username,
            'online_users': get_online_users_list()
        }, room='general')
        
        print(f"User {username} connected")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection"""
    if 'user_id' in session:
        user_id = str(session['user_id'])
        username = session['username']
        
        # Remove from online users
        if user_id in online_users:
            del online_users[user_id]
        
        # Notify others
        emit('user_offline', {
            'user_id': user_id,
            'username': username,
            'online_users': get_online_users_list()
        }, room='general')
        
        print(f"User {username} disconnected")

@socketio.on('send_private_message')
def handle_private_message(data):
    """Handle private chat message"""
    if 'user_id' not in session:
        return
    
    message = data.get('message', '').strip()
    recipient = data.get('recipient', '')
    message_type = data.get('type', 'text')
    
    if not message or not recipient:
        return
    
    user_id = session['user_id']
    username = session['username']
    
    # Save private message to database
    save_private_message_to_db(user_id, username, recipient, message, message_type, data)
    
    # Create message data
    message_data = {
        'sender': username,
        'recipient': recipient,
        'message': message,
        'type': message_type,
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'user_id': str(user_id)
    }
    
    # Add extra data for special message types
    if message_type == 'emotion' and 'emotion_data' in data:
        message_data['extra_data'] = json.dumps(data['emotion_data'])
    elif message_type == 'mood_filter' and 'mood_data' in data:
        message_data['extra_data'] = json.dumps(data['mood_data'])
    
    # Send to sender
    emit('receive_private_message', message_data)
    
    # Send to recipient if they're online and it's not a self-message
    if recipient != username:
        recipient_socket = get_user_socket(recipient)
        if recipient_socket:
            emit('receive_private_message', message_data, room=recipient_socket)

@socketio.on('get_chat_history')
def handle_get_chat_history(data):
    """Get chat history between two users"""
    if 'user_id' not in session:
        return
    
    recipient = data.get('recipient', '')
    if not recipient:
        return
    
    username = session['username']
    
    # Get chat history from database
    messages = get_chat_history_from_db(username, recipient)
    
    emit('chat_history', {'messages': messages})

@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining a room"""
    if 'user_id' not in session:
        return
    
    room = data.get('room', 'general')
    user_id = str(session['user_id'])
    username = session['username']
    
    # Leave current room
    if user_id in online_users:
        current_room = online_users[user_id]['room']
        leave_room(current_room)
    
    # Join new room
    join_room(room)
    online_users[user_id]['room'] = room
    
    emit('room_joined', {'room': room, 'username': username}, room=room)

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    print("=" * 50)
    print("🚀 ChatApp Starting...")
    print("=" * 50)
    print("✓ Real-time chat with Socket.IO")
    print("✓ User authentication & registration") 
    print("✓ Online user status")
    print("✓ Profile management")
    if EMOTION_AVAILABLE:
        print(f"✓ Emotion detection ({EMOTION_METHOD})")
    else:
        print("⚠ Emotion detection disabled")
    print("🎨 MOOD filters coming soon")
    print("✓ Dark themed UI")
    print("=" * 50)
    
    # Get port and environment
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    if IS_RENDER:
        print(f"🌐 Running on Render - Port: {port}")
    else:
        print(f"🌐 Local server: http://localhost:{port}")
    
    print("=" * 50)
    
    # Run the application
    socketio.run(app, debug=debug_mode, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)