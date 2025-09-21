#!/usr/bin/env python3

"""
Visual Demo - Contributor and Developer Links
Shows the application with both contributor and developer links
"""

import sys
from PySide6.QtWidgets import QApplication
from datetime import datetime

def visual_demo():
    """Visual demonstration of both links"""
    print("🎯 Visual Demo - Contributor & Developer Links")
    print("=" * 50)
    
    try:
        from script import LaptopTestingApp
        
        # Create QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create and show main window
        print("📱 Opening application with both contributor and developer links...")
        main_window = LaptopTestingApp()
        main_window.show()
        
        # Update status to show the layout clearly
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        main_window.status_label.setText(f"Demo mode - Time: {timestamp}")
        
        print("\n✅ Application opened successfully!")
        print("📊 Visual Layout Check:")
        print("  • Look at the BOTTOM of the window")
        print("  • LEFT: Status message")
        print("  • RIGHT: Two clickable links")
        print()
        print("🔗 Link Details:")
        print("  • 'Contributor' (GREEN) → https://github.com/bibekchandsah/pc-checker")
        print("  • 'Developed by Bibek' (BLUE) → https://www.bibekchandsah.com.np/")
        print()
        print("🎯 Test Instructions:")
        print("  1. Hover over both links to see color changes")
        print("  2. Click 'Contributor' to open GitHub repository")
        print("  3. Click 'Developed by Bibek' to open personal website")
        print("  4. Check tooltips when hovering")
        print()
        print("📋 Expected Layout:")
        print("  [Status Message]                    [Contributor | Developed by Bibek]")
        print()
        print("🎉 Close the window when finished testing!")
        
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    visual_demo()