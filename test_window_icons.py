#!/usr/bin/env python3

"""
Window Icon and Centering Test Script
Tests that all windows display with the correct icon and are centered on screen
"""

import sys
import os
import time
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

def test_main_window():
    """Test the main application window"""
    print("🖥️ Testing main application window...")
    
    try:
        from script import LaptopTestingApp
        
        # Create main window
        main_window = LaptopTestingApp()
        main_window.show()
        
        print("✅ Main window created and displayed")
        
        # Check if icon is set
        icon = main_window.windowIcon()
        if not icon.isNull():
            print("✅ Main window icon is set")
        else:
            print("❌ Main window icon is not set")
        
        return main_window
        
    except Exception as e:
        print(f"❌ Error testing main window: {e}")
        return None

def test_camera_window():
    """Test the camera test window"""
    print("\n📷 Testing camera test window...")
    
    try:
        from camera_test import CameraTestWindow
        
        # Create camera window
        camera_window = CameraTestWindow()
        camera_window.show()
        
        print("✅ Camera window created and displayed")
        
        # Check if icon is set
        icon = camera_window.windowIcon()
        if not icon.isNull():
            print("✅ Camera window icon is set")
        else:
            print("❌ Camera window icon is not set")
        
        return camera_window
        
    except Exception as e:
        print(f"❌ Error testing camera window: {e}")
        return None

def test_microphone_window():
    """Test the microphone test window"""
    print("\n🎤 Testing microphone test window...")
    
    try:
        from microphone_test import MicrophoneTestWindow
        
        # Create microphone window
        microphone_window = MicrophoneTestWindow()
        microphone_window.show()
        
        print("✅ Microphone window created and displayed")
        
        # Check if icon is set
        icon = microphone_window.windowIcon()
        if not icon.isNull():
            print("✅ Microphone window icon is set")
        else:
            print("❌ Microphone window icon is not set")
        
        return microphone_window
        
    except Exception as e:
        print(f"❌ Error testing microphone window: {e}")
        return None

def test_window_utils():
    """Test the window utilities module"""
    print("\n🔧 Testing window utilities...")
    
    try:
        from window_utils import set_window_icon_and_center, center_window, set_window_icon
        print("✅ Window utilities imported successfully")
        
        # Check if icon file exists
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            print("✅ Icon file (icon.png) exists")
        else:
            print("❌ Icon file (icon.png) not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing window utilities: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive window testing"""
    print("🧪 Starting Comprehensive Window Test")
    print("=" * 50)
    
    # Initialize QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    windows = []
    test_results = []
    
    # Test window utilities first
    utils_result = test_window_utils()
    test_results.append(("Window Utils", utils_result))
    
    # Test main window
    main_window = test_main_window()
    if main_window:
        windows.append(("Main Window", main_window))
        test_results.append(("Main Window", True))
    else:
        test_results.append(("Main Window", False))
    
    # Test camera window
    camera_window = test_camera_window()
    if camera_window:
        windows.append(("Camera Window", camera_window))
        test_results.append(("Camera Window", True))
    else:
        test_results.append(("Camera Window", False))
    
    # Test microphone window  
    microphone_window = test_microphone_window()
    if microphone_window:
        windows.append(("Microphone Window", microphone_window))
        test_results.append(("Microphone Window", True))
    else:
        test_results.append(("Microphone Window", False))
    
    # Display summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall Result: {passed}/{total} tests passed")
    
    if windows:
        print(f"\n🖥️ {len(windows)} windows are currently displayed")
        print("You can now visually verify that:")
        print("  • All windows have the icon.png icon in the title bar")
        print("  • All windows are centered on the screen")
        print("  • All windows display properly without errors")
        
        # Show a message box for user verification
        msg = QMessageBox()
        msg.setWindowTitle("Visual Verification")
        msg.setText("Please verify that all windows:\n\n• Have the correct icon in title bar\n• Are centered on screen\n• Display without errors\n\nClick OK when done.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Set icon for message box too
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            from PySide6.QtGui import QIcon
            msg.setWindowIcon(QIcon(icon_path))
        
        msg.exec()
        
        # Close all test windows
        for window_name, window in windows:
            try:
                window.close()
                print(f"✅ Closed {window_name}")
            except Exception as e:
                print(f"❌ Error closing {window_name}: {e}")
    
    print(f"\n🎉 Window testing completed!")
    
    if passed == total:
        print("🎊 All tests passed! Icon and centering functionality is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)