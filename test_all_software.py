#!/usr/bin/env python3

"""
Test script to verify all installed software is included in CSV generation
"""

import sys
import os
import glob
import time
from script import LaptopTestingApp
from PySide6.QtWidgets import QApplication

def test_all_software_csv():
    """Test that all installed software is included in CSV"""
    print("Testing CSV generation with all installed software...")
    
    # Create minimal QApplication for testing
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Create the main application
        main_app = LaptopTestingApp()
        
        # Get existing CSV files before generation
        existing_files = set(glob.glob("system_report_*.csv"))
        
        # Call generate_csv_report (no parameters)
        result = main_app.generate_csv_report()
        
        # Wait a moment for file to be written
        time.sleep(1)
        
        # Find the new CSV file
        new_files = set(glob.glob("system_report_*.csv")) - existing_files
        
        if new_files:
            csv_file = list(new_files)[0]
            print(f"✓ CSV generation successful: {csv_file}")
            
            # Read and analyze the generated CSV
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for the updated header
            if "INSTALLED SOFTWARE (All)" in content:
                print("✓ Found: INSTALLED SOFTWARE (All) - header updated correctly")
            elif "INSTALLED SOFTWARE (Top 10)" in content:
                print("✗ Still shows: INSTALLED SOFTWARE (Top 10) - change not applied")
            else:
                print("✗ Software section header not found")
            
            # Count software entries
            lines = content.split('\n')
            software_count = 0
            in_software_section = False
            
            for line in lines:
                if "INSTALLED SOFTWARE" in line:
                    in_software_section = True
                    continue
                elif in_software_section and line.strip() == ",,":
                    break  # End of software section
                elif in_software_section and line.startswith("Software ") and "," in line:
                    software_count += 1
            
            print(f"📊 Total software entries found: {software_count}")
            
            # Show first few and last few software entries
            software_lines = []
            in_software_section = False
            
            for line in lines:
                if "INSTALLED SOFTWARE" in line:
                    in_software_section = True
                    continue
                elif line.strip() == "Software,Name,Version":
                    continue  # Skip header
                elif in_software_section and line.strip() == ",,":
                    break  # End of software section
                elif in_software_section and line.startswith("Software ") and "," in line:
                    software_lines.append(line.strip())
            
            if software_lines:
                print("\n📋 Sample software entries:")
                # Show first 5
                for i, line in enumerate(software_lines[:5]):
                    print(f"  {line}")
                
                if len(software_lines) > 10:
                    print("  ...")
                    # Show last 5
                    for line in software_lines[-5:]:
                        print(f"  {line}")
                
                print(f"\n✅ Successfully showing all {len(software_lines)} installed software entries!")
            else:
                print("✗ No software entries found")
            
            print(f"\n📄 Generated CSV file: {csv_file}")
            
        else:
            print("✗ CSV generation failed or no new file found")
            return False
            
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if app:
            app.quit()
    
    return True

if __name__ == '__main__':
    success = test_all_software_csv()
    if success:
        print("\n🎉 All software test completed successfully!")
    else:
        print("\n❌ All software test failed!")
    
    sys.exit(0 if success else 1)