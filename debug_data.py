#!/usr/bin/env python3
"""
Debug script to check the actual data structure returned by hardware and OS modules
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from hardware_info import HardwareInfo
from os_info import OSInfo

def debug_data_structures():
    """Debug the data structures to understand the format"""
    print("Debugging Data Structures...")
    print("=" * 50)
    
    try:
        # Initialize modules
        hw_info = HardwareInfo()
        os_info = OSInfo()
        
        print("🔍 Getting hardware data...")
        hw_data = hw_info.get_all_info()
        
        print("📊 Hardware data structure:")
        print(f"Type: {type(hw_data)}")
        print(f"Keys: {list(hw_data.keys()) if isinstance(hw_data, dict) else 'Not a dict'}")
        
        # Check each hardware component
        for key, value in hw_data.items():
            print(f"\n{key}:")
            print(f"  Type: {type(value)}")
            if isinstance(value, dict):
                print(f"  Keys: {list(value.keys())}")
            elif isinstance(value, list):
                print(f"  Length: {len(value)}")
                if value:
                    print(f"  First item type: {type(value[0])}")
                    if isinstance(value[0], dict):
                        print(f"  First item keys: {list(value[0].keys())}")
            else:
                print(f"  Value: {value}")
        
        print("\n" + "=" * 50)
        print("🔍 Getting OS data...")
        os_data = os_info.get_all_os_info()
        
        print("📊 OS data structure:")
        print(f"Type: {type(os_data)}")
        print(f"Keys: {list(os_data.keys()) if isinstance(os_data, dict) else 'Not a dict'}")
        
        # Check each OS component
        for key, value in os_data.items():
            print(f"\n{key}:")
            print(f"  Type: {type(value)}")
            if isinstance(value, dict):
                print(f"  Keys: {list(value.keys())}")
            elif isinstance(value, list):
                print(f"  Length: {len(value)}")
                if value:
                    print(f"  First item type: {type(value[0])}")
                    if isinstance(value[0], dict):
                        print(f"  First item keys: {list(value[0].keys())}")
            else:
                print(f"  Value type: {type(value)}")
        
        print("\n🎯 Finished debugging data structures!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during debugging: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_data_structures()