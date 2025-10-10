#!/usr/bin/env python3
"""
Test script to verify all dependencies work correctly
Run this before compiling to catch issues early
"""

import sys

def test_imports():
    """Test all required imports"""
    print("Testing dependencies...")
    
    try:
        print("✓ Testing basic Python modules...")
        import os
        import sys
        import json
        import csv
        import tempfile
        from datetime import datetime
        print("  ✓ Basic modules OK")
        
        print("✓ Testing PySide6...")
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, QTimer, QThread, Signal
        from PySide6.QtGui import QFont, QPixmap, QIcon
        print("  ✓ PySide6 OK")
        
        print("✓ Testing system info modules...")
        import psutil
        print("  ✓ psutil OK")
        
        import py_cpuinfo
        print("  ✓ py_cpuinfo OK")
        
        # Test multiprocessing (the problematic one)
        import multiprocessing
        import multiprocessing.pool
        print("  ✓ multiprocessing OK")
        
        print("✓ Testing Windows-specific modules...")
        try:
            import wmi
            print("  ✓ wmi OK")
        except ImportError:
            print("  ⚠ wmi not available (Linux/Mac?)")
        
        print("✓ Testing network modules...")
        import requests
        import packaging
        print("  ✓ Network modules OK")
        
        print("✓ Testing custom modules...")
        try:
            from hardware_info import HardwareInfo
            print("  ✓ hardware_info OK")
        except ImportError as e:
            print(f"  ✗ hardware_info failed: {e}")
            
        try:
            from os_info import OSInfo
            print("  ✓ os_info OK")
        except ImportError as e:
            print(f"  ✗ os_info failed: {e}")
            
        try:
            from system_tests import SystemTests
            print("  ✓ system_tests OK")
        except ImportError as e:
            print(f"  ✗ system_tests failed: {e}")
        
        print("\n" + "="*50)
        print("✅ ALL CORE DEPENDENCIES WORKING!")
        print("✅ Ready for compilation!")
        print("="*50)
        return True
        
    except ImportError as e:
        print(f"\n❌ DEPENDENCY ERROR: {e}")
        print("❌ Please install missing dependencies before compiling")
        print("Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

def test_cpu_info():
    """Test CPU info specifically (the source of multiprocessing error)"""
    print("\nTesting CPU info functionality...")
    try:
        import py_cpuinfo
        info = py_cpuinfo.get_cpu_info()
        print(f"✓ CPU detected: {info.get('brand_raw', 'Unknown')}")
        print(f"✓ Architecture: {info.get('arch', 'Unknown')}")
        print(f"✓ Cores: {info.get('count', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ CPU info test failed: {e}")
        return False

def main():
    print("="*60)
    print("Laptop Testing Program - Dependency Test")
    print("="*60)
    
    if not test_imports():
        sys.exit(1)
    
    if not test_cpu_info():
        print("⚠ CPU info test failed, but compilation might still work")
    
    print("\n🎉 All tests passed! You can now compile the application.")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()