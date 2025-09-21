"""
Test the fixed microphone test functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
import time

def main():
    """Test the microphone functionality with fixes"""
    print("🎤 Testing Fixed Microphone Test")
    print("=" * 40)
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Import and create microphone test window
        from microphone_test import MicrophoneTestWindow
        
        print("Creating microphone test window...")
        window = MicrophoneTestWindow()
        window.show()
        
        print("✅ Microphone test window opened!")
        print("\nFixed Issues:")
        print("• Math error in volume calculation (sqrt of negative values)")
        print("• UI freezing due to too frequent waveform updates")
        print("• Better thread cleanup and error handling")
        print("• Throttled waveform updates (50ms interval)")
        print("• Improved data validation and safety checks")
        
        print("\nInstructions:")
        print("• Click 'Start Recording' to test the fixes")
        print("• The waveform should update smoothly without freezing")
        print("• No more math errors should appear in console")
        print("• Volume level should display correctly")
        print("• Window should close properly without hanging")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Error running test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()