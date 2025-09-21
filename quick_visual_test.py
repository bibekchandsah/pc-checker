#!/usr/bin/env python3

"""
Quick Visual Test - Developer Credit Position
Shows the application with the new developer credit position
"""

import sys
from PySide6.QtWidgets import QApplication
from datetime import datetime

def quick_visual_test():
    """Quick visual test of the new position"""
    print("🎯 Quick Visual Test - Developer Credit Position")
    print("=" * 50)
    
    try:
        from script import LaptopTestingApp
        
        # Create QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create and show main window
        print("📱 Opening application with new developer credit position...")
        main_window = LaptopTestingApp()
        main_window.show()
        
        # Update status to show the positioning clearly
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        main_window.status_label.setText(f"Ready - Last check: {timestamp}")
        
        print("\n✅ Application opened successfully!")
        print("📊 Visual Check:")
        print("  • Look at the bottom of the window")
        print("  • Status message should be on the LEFT")
        print("  • 'Developed by Bibek' should be on the RIGHT")
        print("  • Both should be in the same bottom row")
        print("  • Developer credit should be clickable with hover effect")
        print()
        print("🎯 Please verify visually and close the window when done")
        
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    quick_visual_test()