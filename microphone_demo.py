"""
Microphone Test Demo
Quick demonstration of the microphone test functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication

def main():
    """Run microphone test demo"""
    print("🎤 Microphone Test Demo")
    print("=" * 30)
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Import and create microphone test window
        from microphone_test import MicrophoneTestWindow
        
        print("Creating microphone test window...")
        window = MicrophoneTestWindow()
        window.show()
        
        print("✅ Microphone test window opened!")
        print("\nInstructions:")
        print("• Click 'Start Recording' to begin microphone capture")
        print("• Speak or make sounds to see waveform visualization")
        print("• Check volume level bar for input sensitivity")
        print("• Use 'Test System Audio' to verify speakers")
        print("• Use settings buttons for microphone configuration")
        print("• Close window when done testing")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Error running microphone test demo: {e}")
        print("\nPossible solutions:")
        print("• Install missing packages: pip install pyaudio matplotlib numpy")
        print("• Check microphone permissions")
        print("• Verify audio drivers are installed")

if __name__ == "__main__":
    main()