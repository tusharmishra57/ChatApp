"""
Lightweight emotion detector using FER for Render deployment
Fallback for when the main emotion_detector.py is not available
"""

import cv2
import numpy as np
import base64
from PIL import Image
import io

try:
    from fer import FER
    FER_AVAILABLE = True
except ImportError:
    FER_AVAILABLE = False

class LightweightEmotionDetector:
    """Lightweight emotion detector for Render"""
    
    def __init__(self):
        if FER_AVAILABLE:
            self.detector = FER(mtcnn=True)
        else:
            self.detector = None
    
    def detect_emotion_from_image_data(self, image_data):
        """Detect emotion from base64 image data"""
        if not FER_AVAILABLE or not self.detector:
            return {
                'success': False,
                'message': 'Emotion detection not available'
            }
        
        try:
            # Decode base64 image
            if 'data:image' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Detect emotions
            emotions = self.detector.detect_emotions(image_cv)
            
            if emotions and len(emotions) > 0:
                # Get dominant emotion
                emotion_scores = emotions[0]['emotions']
                dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
                
                emotion_name = dominant_emotion[0]
                confidence = dominant_emotion[1] * 100
                
                # Map emotion names
                emotion_map = {
                    'angry': 'angry',
                    'disgust': 'disgusted', 
                    'fear': 'fearful',
                    'happy': 'happy',
                    'sad': 'sad',
                    'surprise': 'surprised',
                    'neutral': 'neutral'
                }
                
                emotion_display = emotion_map.get(emotion_name, emotion_name)
                
                # Get emoji
                emoji_map = {
                    'angry': '😠',
                    'disgusted': '🤢',
                    'fearful': '😨',
                    'happy': '😊',
                    'sad': '😢',
                    'surprised': '😲',
                    'neutral': '😐'
                }
                
                emoji = emoji_map.get(emotion_display, '😐')
                
                return {
                    'success': True,
                    'emotion': emotion_display,
                    'confidence': confidence,
                    'message': f'Detected {emotion_display} with {confidence:.1f}% confidence',
                    'emoji': emoji,
                    'all_emotions': emotion_scores
                }
            else:
                return {
                    'success': False,
                    'message': 'No face detected in the image'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }
    
    def detect_emotion_from_camera(self):
        """Fallback method for compatibility"""
        return {
            'success': False,
            'message': 'Camera detection not available. Please use the web interface.'
        }