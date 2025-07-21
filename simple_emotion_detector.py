"""
Simplified Emotion Detector for ChatApp
Works with basic OpenCV and provides simulated emotion detection
"""

import cv2
import numpy as np
import time
import random
import os
from datetime import datetime

class EmotionDetector:
    """Simplified emotion detection system"""
    
    def __init__(self):
        self.emotions = ['happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'neutral']
        self.emotion_emojis = {
            'happy': '😊',
            'sad': '😢', 
            'angry': '😠',
            'surprise': '😲',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐'
        }
        
        # Face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        print("✓ Simplified Emotion Detector initialized")
    
    def detect_emotion_from_camera(self):
        """Capture image from camera and detect emotion"""
        try:
            # Open camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {
                    'success': False,
                    'message': 'Could not access camera'
                }
            
            print("Camera opened. Press SPACE to capture or ESC to cancel...")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect faces
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                # Draw rectangles around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                
                # Add instructions
                cv2.putText(frame, "Press SPACE to capture emotion", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Faces detected: {len(faces)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('Emotion Detection', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord(' '):  # Space to capture
                    if len(faces) > 0:
                        # Simulate emotion detection
                        emotion = random.choice(self.emotions)
                        confidence = random.uniform(75.0, 95.0)
                        
                        # Save captured image
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"emotion_capture_{timestamp}.jpg"
                        filepath = os.path.join("static", "emotion_captures", filename)
                        os.makedirs(os.path.dirname(filepath), exist_ok=True)
                        cv2.imwrite(filepath, frame)
                        
                        cap.release()
                        cv2.destroyAllWindows()
                        
                        return {
                            'success': True,
                            'emotion': emotion,
                            'confidence': confidence,
                            'message': f'Detected {emotion} with {confidence:.1f}% confidence',
                            'image_path': filepath,
                            'emoji': self.emotion_emojis.get(emotion, '😐')
                        }
                    else:
                        cv2.putText(frame, "No face detected! Please position your face in view.", (10, 90), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        
                elif key == 27:  # ESC to cancel
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            return {
                'success': False,
                'message': 'Emotion detection cancelled'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error during emotion detection: {str(e)}'
            }

def test_emotion_detector():
    """Test the emotion detector"""
    detector = EmotionDetector()
    result = detector.detect_emotion_from_camera()
    print("Result:", result)

if __name__ == "__main__":
    test_emotion_detector()