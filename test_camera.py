#!/usr/bin/env python3
"""
Simple Camera Test Demo
This script demonstrates the camera testing functionality
"""

from system_tests import SystemTests
import time

def main():
    print("📷 Camera Test Demo")
    print("=" * 40)
    
    # Create system tests instance
    tests = SystemTests()
    
    # Callback function to show progress
    def progress_callback(results):
        status = results.get('status', 'Unknown')
        progress = results.get('progress', 0)
        
        print(f"Status: {status}, Progress: {progress}%")
        
        # Show instructions
        if 'instructions' in results and results['instructions']:
            for instruction in results['instructions']:
                print(f"  {instruction}")
        
        # Show errors if any
        if results.get('errors'):
            for error in results['errors']:
                print(f"  ⚠ Error: {error}")
    
    print("Starting camera test...")
    print("This test will attempt to open your camera!")
    print()
    
    # Start the test
    test_results = tests.camera_test(callback=progress_callback)
    
    # Wait for test completion
    while tests.is_testing:
        time.sleep(1)
    
    print()
    print("📷 Camera Test Complete!")
    
    # Show final results
    if test_results.get('camera_opened'):
        print("✅ Camera application opened successfully!")
        print("Please verify that:")
        print("• Camera preview is showing live video")
        print("• Image quality is clear and not distorted")
        print("• Camera responds to different lighting conditions")
    else:
        print("❌ Camera test failed")
        print("Possible issues:")
        print("• No camera hardware detected")
        print("• Camera drivers not installed")
        print("• Camera blocked by privacy settings")
        print("• Camera in use by another application")
    
    print()
    print("💡 Tips:")
    print("• Check Windows Privacy settings for camera access")
    print("• Ensure camera drivers are installed and up to date")
    print("• Close other applications that might be using the camera")
    print("• Try manually opening the Camera app from Start menu")

if __name__ == "__main__":
    main()