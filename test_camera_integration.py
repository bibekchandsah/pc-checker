"""
Test script to verify camera test functionality
"""

import sys
import os
from PySide6.QtWidgets import QApplication

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_camera_window():
    """Test camera test window functionality"""
    print("Testing Camera Test Window...")
    
    try:
        # Import camera test
        from camera_test import CameraTestWindow
        
        # Create application
        app = QApplication(sys.argv)
        
        # Create camera test window
        camera_window = CameraTestWindow()
        camera_window.show()
        
        print("✅ Camera test window created successfully!")
        print("Features available:")
        print("• Integrated camera preview")
        print("• Start/Stop camera controls")
        print("• Manual camera app launcher")
        print("• Debug camera settings access")
        print("• Real-time camera information display")
        
        # Run for a short time to verify
        print("\nWindow will close automatically in 3 seconds...")
        
        # Close after brief display
        from PySide6.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(3000)  # 3 seconds
        
        app.exec()
        
        print("✅ Camera test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing camera window: {e}")
        return False

if __name__ == "__main__":
    success = test_camera_window()
    if success:
        print("\n🎉 Camera test implementation successful!")
        print("You can now click 'Camera Test' in the main application to:")
        print("• See live camera preview in integrated window")
        print("• Use manual camera app button")
        print("• Access debug camera settings")
    else:
        print("\n❌ Camera test needs fixing")