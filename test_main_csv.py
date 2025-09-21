#!/usr/bin/env python3
"""
Integration test for the CSV generation feature in the main application
This script simulates clicking the "Generate Report" button
"""

import sys
import os
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(__file__))

def test_main_app_csv():
    """Test the main application's CSV generation"""
    print("Testing Main Application CSV Generation...")
    print("=" * 50)
    
    try:
        # Import the main application classes
        from script import LaptopTestingApp
        from PySide6.QtWidgets import QApplication
        
        # Create a QApplication instance (required for Qt)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        print("📱 Creating main application instance...")
        main_app = LaptopTestingApp()
        
        print("⏳ Loading initial data...")
        # Simulate some data loading time
        import time
        time.sleep(2)
        
        print("📊 Testing CSV report generation...")
        
        # Call the CSV generation method directly
        main_app.generate_csv_report()
        
        print("✅ CSV generation method called successfully!")
        print("💡 Check for CSV files in the current directory")
        
        # List any CSV files created today
        current_date = datetime.now().strftime("%Y%m%d")
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and current_date in f]
        
        if csv_files:
            print(f"\n📄 CSV files found ({len(csv_files)}):")
            for csv_file in csv_files:
                size = os.path.getsize(csv_file)
                print(f"  • {csv_file} ({size} bytes)")
        else:
            print("\n📄 No CSV files found with today's date")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing main app CSV generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("Main Application CSV Generation Test")
    print("=" * 50)
    
    success = test_main_app_csv()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Main application CSV generation test completed!")
        print("🎯 You can now run the main application and click 'Generate Report'")
    else:
        print("❌ Test failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    # Don't exit here to prevent Qt from continuing to run
    print(f"\nTest result: {'SUCCESS' if success else 'FAILED'}")