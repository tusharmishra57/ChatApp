"""
Database configuration for ChatApp - Render deployment
Supports both SQLite (development) and PostgreSQL (production)
"""

import os
import sqlite3
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

def get_db_connection():
    """Get database connection based on environment"""
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///chat_app.db')
    
    if database_url.startswith('postgresql://') or database_url.startswith('postgres://'):
        if not POSTGRES_AVAILABLE:
            raise ImportError("psycopg2 not installed")
        
        # PostgreSQL connection for production (Render)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        return conn, 'postgresql'
    else:
        # SQLite connection for local development
        db_path = database_url.replace('sqlite:///', '')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn, 'sqlite'

def init_database():
    """Initialize database tables"""
    conn, db_type = get_db_connection()
    
    try:
        cursor = conn.cursor()
        
        if db_type == 'postgresql':
            # PostgreSQL tables for production
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    profile_picture VARCHAR(255) DEFAULT 'default_avatar.png',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_online INTEGER DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    username VARCHAR(80) NOT NULL,
                    room VARCHAR(80) NOT NULL DEFAULT 'general',
                    message TEXT NOT NULL,
                    message_type VARCHAR(50) DEFAULT 'text',
                    extra_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emotions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    emotion VARCHAR(50) NOT NULL,
                    confidence REAL,
                    image_path VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
        else:
            # SQLite tables for local development
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    profile_picture TEXT DEFAULT 'default_avatar.png',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_online INTEGER DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    room TEXT NOT NULL DEFAULT 'general',
                    message TEXT NOT NULL,
                    message_type TEXT DEFAULT 'text',
                    extra_data TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emotions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    emotion TEXT NOT NULL,
                    confidence REAL,
                    image_path TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
        
        conn.commit()
        print("✓ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_db_connection_simple():
    """Simplified connection for existing code"""
    conn, _ = get_db_connection()
    return conn