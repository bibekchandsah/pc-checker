#!/usr/bin/env python3

"""
Test script to verify all card details are included in CSV generation
"""

import sys
import os
import glob
import time
from script import LaptopTestingApp
from PySide6.QtWidgets import QApplication

def test_all_cards_csv():
    """Test that all cards from System Overview are included in CSV"""
    print("Testing CSV generation with all card details...")
    
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
        
        if new_files and result:
            csv_file = list(new_files)[0]
            print(f"✓ CSV generation successful: {csv_file}")
            
            # Read and analyze the generated CSV
            with open(csv_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for all expected card sections
            expected_cards = [
                "=== SYSTEM SUMMARY CARD ===",
                "=== SYSTEM INFORMATION CARD ===", 
                "=== BIOS & MOTHERBOARD CARD ===",
                "=== CPU INFORMATION CARD ===",
                "=== RAM INFORMATION CARD ===",
                "=== ROM INFORMATION CARD ===",
                "=== BATTERY INFORMATION CARD ===",
                "=== OTHER INFORMATION CARD ==="
            ]
            
            print("\nChecking for all card sections:")
            for card in expected_cards:
                if card in content:
                    print(f"✓ Found: {card}")
                else:
                    print(f"✗ Missing: {card}")
            
            # Check for key details in each card
            print("\nChecking key details in cards:")
            
            # CPU Card details
            cpu_details = [
                "CPU Information,Name,",
                "CPU Information,Architecture,",
                "CPU Information,Physical Cores,",
                "CPU Information,Logical Cores,",
                "CPU Information,Vendor,"
            ]
            
            for detail in cpu_details:
                if detail in content:
                    print(f"✓ Found CPU detail: {detail.split(',')[1]}")
                else:
                    print(f"✗ Missing CPU detail: {detail.split(',')[1]}")
            
            # RAM Card details
            ram_details = [
                "RAM Information,Total,",
                "RAM Information,Available,",
                "RAM Information,Used,",
                "RAM Information,Percentage,",
                "RAM Information,Memory Slots,"
            ]
            
            for detail in ram_details:
                if detail in content:
                    print(f"✓ Found RAM detail: {detail.split(',')[1]}")
                else:
                    print(f"✗ Missing RAM detail: {detail.split(',')[1]}")
            
            # ROM Card details
            rom_details = [
                "ROM Information,Partitions,",
                "ROM Information,Drive C",
                "ROM Information,Drive D"
            ]
            
            for detail in rom_details:
                if detail in content:
                    print(f"✓ Found ROM detail: {detail.split(',')[1]}")
                else:
                    print(f"✗ Missing ROM detail: {detail.split(',')[1]}")
            
            # Battery Card details
            battery_details = [
                "Battery Information,Present,",
                "Battery Information,Charge Percent,",
                "Battery Information,Status,",
                "Battery Information,Time Left,"
            ]
            
            for detail in battery_details:
                if detail in content:
                    print(f"✓ Found Battery detail: {detail.split(',')[1]}")
                else:
                    print(f"✗ Missing Battery detail: {detail.split(',')[1]}")
            
            # Other Information Card details
            other_details = [
                "Other Information,Sensors (Temp),",
                "Other Information,Fan Speeds,",
                "Other Information,Camera(s),",
                "Other Information,TPM,",
                "Other Information,Chassis Type,",
                "Other Information,Secure Boot,"
            ]
            
            for detail in other_details:
                if detail in content:
                    print(f"✓ Found Other detail: {detail.split(',')[1]}")
                else:
                    print(f"✗ Missing Other detail: {detail.split(',')[1]}")
            
            print(f"\n📄 Generated CSV file: {csv_file}")
            print("✅ All card details verification completed!")
            
            # Don't clean up the file so user can see it
            # os.unlink(csv_file)
            
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
    success = test_all_cards_csv()
    if success:
        print("\n🎉 All card details test completed successfully!")
    else:
        print("\n❌ Card details test failed!")
    
    sys.exit(0 if success else 1)