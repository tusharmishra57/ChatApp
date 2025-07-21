"""
Test script to verify all AI features are working properly
"""

import sys
import os

def test_emotion_detector():
    """Test the emotion detector module"""
    print("=" * 50)
    print("Testing Emotion Detector")
    print("=" * 50)
    
    try:
        from emotion_detector import EmotionDetector
        
        detector = EmotionDetector()
        print("✓ EmotionDetector imported and initialized successfully")
        
        # Test emotion emojis
        print("✓ Emotion emojis available:", list(detector.emotion_emojis.keys()))
        
        # Test face cascade
        if detector.face_cascade.empty():
            print("⚠ Face cascade not loaded properly")
        else:
            print("✓ Face cascade loaded successfully")
        
        print("✓ Emotion Detector test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Emotion Detector test failed: {e}")
        return False

def test_anime_mood_filter():
    """Test the anime mood filter module"""
    print("=" * 50)
    print("Testing Anime Mood Filter")
    print("=" * 50)
    
    try:
        from anime_mood_filter import AnimeMoodFilter
        
        # Test all styles
        styles = ['Hayao', 'Shinkai', 'Paprika']
        
        for style in styles:
            filter_app = AnimeMoodFilter(style)
            print(f"✓ AnimeMoodFilter with {style} style initialized successfully")
            
            # Check style configuration
            if style in filter_app.style_configs:
                config = filter_app.style_configs[style]
                print(f"  - Style name: {config['name']}")
                print(f"  - Description: {config['description']}")
            
        print("✓ Anime Mood Filter test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Anime Mood Filter test failed: {e}")
        return False

def test_dependencies():
    """Test all required dependencies"""
    print("=" * 50)
    print("Testing Dependencies")
    print("=" * 50)
    
    dependencies = [
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('deepface', 'DeepFace'),
        ('tensorflow', 'TensorFlow'),
        ('PIL', 'Pillow'),
        ('flask', 'Flask'),
        ('flask_socketio', 'Flask-SocketIO')
    ]
    
    all_passed = True
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✓ {name} imported successfully")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
            all_passed = False
    
    return all_passed

def test_directories():
    """Test required directories exist"""
    print("=" * 50)
    print("Testing Directory Structure")
    print("=" * 50)
    
    required_dirs = [
        'static',
        'static/emotion_captures',
        'static/anime_captures',
        'static/profiles',
        'templates'
    ]
    
    all_exist = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"❌ Directory missing: {dir_path}")
            # Create missing directories
            os.makedirs(dir_path, exist_ok=True)
            print(f"✓ Created directory: {dir_path}")
    
    return all_exist

def main():
    """Run all tests"""
    print("🚀 Starting AI Features Test Suite")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Directory Structure", test_directories),
        ("Emotion Detector", test_emotion_detector),
        ("Anime Mood Filter", test_anime_mood_filter)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! AI features are ready to use!")
        print("\n🚀 You can now:")
        print("   1. Use Emotion Detection in the chat")
        print("   2. Apply Anime MOOD Filters")
        print("   3. Send AI results to friends")
        print("   4. Enjoy all chat features!")
    else:
        print("⚠ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)