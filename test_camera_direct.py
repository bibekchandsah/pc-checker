"""
Simple Camera Test - Direct Window Test
Tests camera window creation directly with proper Qt application context
"""

import sys
import os
from PySide6.QtWidgets import QApplication

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_camera_window_direct():
    """Test camera window creation directly"""
    print("🔍 Testing Camera Window Creation...")
    
    # Create Qt application first
    app = QApplication(sys.argv)
    
    try:
        # Import camera test window
        from camera_test import CameraTestWindow
        
        print("✅ Creating camera test window...")
        window = CameraTestWindow()
        
        print("✅ Showing camera test window...")
        window.show()
        
        print("✅ Camera window opened successfully!")
        print("\n📋 Test Instructions:")
        print("1. Click '🎥 Start Camera' to test camera preview")
        print("2. Try '📱 Open Camera App' for system camera")
        print("3. Use '🔧 Debug Camera Settings' for troubleshooting")
        print("4. Close window when testing is complete")
        
        print("\n⚠️ Note: If you see QTimer errors, they should not affect functionality")
        print("💡 The window should remain responsive regardless")
        
        # Keep window open until user closes it
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"\n❌ Error creating camera window: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_camera_window_direct()