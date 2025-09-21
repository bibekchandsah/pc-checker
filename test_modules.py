"""
Test script to verify all modules are working correctly
"""

import sys
import traceback

def test_hardware_info():
    """Test hardware information module"""
    try:
        print("Testing Hardware Info Module...")
        from hardware_info import HardwareInfo
        
        hw = HardwareInfo()
        
        # Test basic functions
        cpu_info = hw.get_cpu_info()
        print(f"✓ CPU Info: {cpu_info.get('name', 'Unknown')}")
        
        memory_info = hw.get_memory_info()
        print(f"✓ Memory Info: {memory_info.get('total', 0)} GB")
        
        system_info = hw.get_system_info()
        print(f"✓ System Info: {system_info.get('system', 'Unknown')}")
        
        return True
    except Exception as e:
        print(f"✗ Hardware Info Error: {e}")
        traceback.print_exc()
        return False

def test_os_info():
    """Test OS information module"""
    try:
        print("\nTesting OS Info Module...")
        from os_info import OSInfo
        
        os_info = OSInfo()
        
        # Test basic functions
        os_details = os_info.get_os_details()
        print(f"✓ OS Details: {os_details.get('system', 'Unknown')}")
        
        network_config = os_info.get_network_configuration()
        print(f"✓ Network Config: {len(network_config.get('adapters', []))} adapters")
        
        return True
    except Exception as e:
        print(f"✗ OS Info Error: {e}")
        traceback.print_exc()
        return False

def test_system_tests():
    """Test system tests module"""
    try:
        print("\nTesting System Tests Module...")
        from system_tests import SystemTests
        
        tests = SystemTests()
        
        # Test recommendations
        sample_hw_info = {'cpu': {'cores_physical': 4}, 'memory': {'total': 8}}
        recommendations = tests.get_test_recommendations(sample_hw_info)
        print(f"✓ Test Recommendations: {len(recommendations)} recommendations")
        
        return True
    except Exception as e:
        print(f"✗ System Tests Error: {e}")
        traceback.print_exc()
        return False

def test_gui_imports():
    """Test GUI imports"""
    try:
        print("\nTesting GUI Imports...")
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        from PySide6.QtGui import QFont
        print("✓ PySide6 imports successful")
        
        return True
    except Exception as e:
        print(f"✗ GUI Import Error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Laptop Testing Program - Module Tests")
    print("=" * 50)
    
    tests = [
        test_hardware_info,
        test_os_info,
        test_system_tests,
        test_gui_imports
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the application, execute: python script.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)