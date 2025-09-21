#!/usr/bin/env python3
"""
Debug network interface structure
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from hardware_info import HardwareInfo

def debug_network_structure():
    """Debug the network interface structure"""
    print("Debugging Network Interface Structure...")
    print("=" * 50)
    
    try:
        hw_info = HardwareInfo()
        hw_data = hw_info.get_all_info()
        
        network_info = hw_data.get('network', {})
        interfaces = network_info.get('interfaces', [])
        
        print(f"Network info type: {type(network_info)}")
        print(f"Interfaces type: {type(interfaces)}")
        print(f"Number of interfaces: {len(interfaces) if isinstance(interfaces, list) else 'N/A'}")
        
        if isinstance(interfaces, list) and interfaces:
            print("\nFirst few interfaces:")
            for i, interface in enumerate(interfaces[:3]):
                print(f"\nInterface {i+1}:")
                print(f"  Type: {type(interface)}")
                if isinstance(interface, dict):
                    print(f"  Keys: {list(interface.keys())}")
                    addresses = interface.get('addresses', [])
                    print(f"  Addresses type: {type(addresses)}")
                    print(f"  Addresses length: {len(addresses) if isinstance(addresses, list) else 'N/A'}")
                    if isinstance(addresses, list) and addresses:
                        print(f"  First address type: {type(addresses[0])}")
                        print(f"  First address content: {addresses[0]}")
                        if len(addresses) > 1:
                            print(f"  Second address type: {type(addresses[1])}")
                            print(f"  Second address content: {addresses[1]}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_network_structure()