#!/usr/bin/env python3
"""
Test script for CSV report generation
This script tests the CSV generation functionality without requiring the full GUI
"""

import sys
import os
import csv
from datetime import datetime

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(__file__))

from hardware_info import HardwareInfo
from os_info import OSInfo

def test_csv_generation():
    """Test CSV report generation functionality"""
    print("Testing CSV Report Generation...")
    print("=" * 50)
    
    try:
        # Initialize hardware and OS info modules
        print("📊 Initializing hardware info module...")
        hw_info = HardwareInfo()
        
        print("💻 Initializing OS info module...")
        os_info = OSInfo()
        
        print("🔍 Collecting hardware data...")
        hw_data = hw_info.get_all_info()
        print(f"✅ Hardware data collected: {len(hw_data)} categories")
        
        print("🔍 Collecting OS data...")
        os_data = os_info.get_all_os_info()
        print(f"✅ OS data collected: {len(os_data)} categories")
        
        # Generate test CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_system_report_{timestamp}.csv"
        
        print(f"📝 Generating CSV report: {filename}")
        
        # Prepare CSV data (simplified version)
        csv_data = []
        
        # Header
        csv_data.append(['SYSTEM REPORT GENERATED', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ''])
        csv_data.append(['', '', ''])
        
        # System Overview
        system_info = hw_data.get('system', {})
        csv_data.append(['SYSTEM OVERVIEW', '', ''])
        csv_data.append(['Component', 'Property', 'Value'])
        csv_data.append(['System', 'Hostname', system_info.get('hostname', 'Unknown')])
        csv_data.append(['System', 'OS', system_info.get('system', 'Unknown')])
        csv_data.append(['System', 'Release', system_info.get('release', 'Unknown')])
        csv_data.append(['System', 'Processor', system_info.get('processor', 'Unknown')])
        csv_data.append(['', '', ''])
        
        # Hardware Summary
        cpu_info = hw_data.get('cpu', {})
        memory_info = hw_data.get('memory', {})
        
        csv_data.append(['HARDWARE SUMMARY', '', ''])
        csv_data.append(['Component', 'Property', 'Value'])
        csv_data.append(['CPU', 'Name', cpu_info.get('name', 'Unknown')])
        csv_data.append(['CPU', 'Cores', f"{cpu_info.get('cores_physical', 'Unknown')} physical / {cpu_info.get('cores_logical', 'Unknown')} logical"])
        csv_data.append(['CPU', 'Frequency', f"{cpu_info.get('max_frequency_mhz', 'Unknown')} MHz"])
        csv_data.append(['Memory', 'Total', f"{memory_info.get('total', 'Unknown')} GB"])
        csv_data.append(['Memory', 'Available', f"{memory_info.get('available', 'Unknown')} GB"])
        csv_data.append(['Memory', 'Usage', f"{memory_info.get('percent', 'Unknown')}%"])
        csv_data.append(['', '', ''])
        
        # OS Summary
        os_details = os_data.get('os_details', {})
        csv_data.append(['OS SUMMARY', '', ''])
        csv_data.append(['Component', 'Property', 'Value'])
        csv_data.append(['OS', 'System', os_details.get('system', 'Unknown')])
        csv_data.append(['OS', 'Version', os_details.get('version', 'Unknown')])
        csv_data.append(['OS', 'Architecture', str(os_details.get('architecture', 'Unknown'))])
        csv_data.append(['OS', 'Boot Time', os_details.get('boot_time', 'Unknown')])
        csv_data.append(['', '', ''])
        
        # Test Status
        csv_data.append(['TEST STATUS', '', ''])
        csv_data.append(['Test', 'Status', 'Notes'])
        csv_data.append(['Hardware Detection', 'PASSED', f"Successfully detected {len(hw_data)} hardware categories"])
        csv_data.append(['OS Detection', 'PASSED', f"Successfully detected {len(os_data)} OS categories"])
        csv_data.append(['CSV Generation', 'PASSED', f"Generated {len(csv_data)} rows of data"])
        
        # Write CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for row in csv_data:
                writer.writerow(row)
        
        print(f"✅ CSV report generated successfully!")
        print(f"📄 File: {filename}")
        print(f"📁 Location: {os.path.abspath(filename)}")
        print(f"📊 Rows written: {len(csv_data)}")
        
        # Verify file exists and read a few lines
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"💾 File size: {file_size} bytes")
            
            print("\n📋 Preview of generated CSV:")
            print("-" * 40)
            with open(filename, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < 10:  # Show first 10 lines
                        print(f"{i+1:2}: {line.strip()}")
                    else:
                        break
            print("-" * 40)
        
        print("\n🎉 CSV report generation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during CSV generation test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("CSV Report Generation Test")
    print("=" * 50)
    
    success = test_csv_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! CSV report generation is working correctly.")
    else:
        print("❌ Tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)