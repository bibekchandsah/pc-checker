"""
Test script for microphone test functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_microphone_import():
    """Test if microphone test can be imported"""
    try:
        from microphone_test import MicrophoneTest, MicrophoneTestWindow
        print("✅ Microphone test imports successful")
        return True
    except Exception as e:
        print(f"❌ Microphone test import error: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are available"""
    dependencies = []
    
    # Test PyAudio
    try:
        import pyaudio
        dependencies.append("✅ PyAudio available")
    except ImportError:
        dependencies.append("❌ PyAudio not available - install: pip install pyaudio")
    
    # Test Matplotlib
    try:
        import matplotlib
        dependencies.append("✅ Matplotlib available")
    except ImportError:
        dependencies.append("❌ Matplotlib not available - install: pip install matplotlib")
    
    # Test NumPy
    try:
        import numpy
        dependencies.append("✅ NumPy available")
    except ImportError:
        dependencies.append("❌ NumPy not available - install: pip install numpy")
    
    # Test SciPy (optional)
    try:
        import scipy
        dependencies.append("✅ SciPy available")
    except ImportError:
        dependencies.append("⚠️ SciPy not available (optional) - install: pip install scipy")
    
    return dependencies

if __name__ == "__main__":
    print("🎤 Microphone Test Verification")
    print("=" * 40)
    
    # Test imports
    import_success = test_microphone_import()
    
    # Test dependencies
    print("\nDependency Check:")
    dependencies = test_dependencies()
    for dep in dependencies:
        print(dep)
    
    # Test microphone test creation
    if import_success:
        try:
            from microphone_test import MicrophoneTest
            mic_test = MicrophoneTest()
            print("\n✅ MicrophoneTest instance created successfully")
        except Exception as e:
            print(f"\n❌ Error creating MicrophoneTest: {e}")
    
    print("\n" + "=" * 40)
    print("Test completed!")