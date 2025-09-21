#!/usr/bin/env python3

"""
Test Contributor Link Addition
Verifies the new contributor link functionality alongside the developer credit
"""

import sys
import time
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

def test_contributor_functionality():
    """Test the new contributor link functionality"""
    print("🎯 Testing Contributor Link Addition")
    print("=" * 40)
    
    try:
        from script import LaptopTestingApp
        
        # Create QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create main window
        print("📱 Creating main application window...")
        main_window = LaptopTestingApp()
        main_window.show()
        
        # Check if both labels exist
        contributor_found = hasattr(main_window, 'contributor_label')
        developer_found = hasattr(main_window, 'developer_label')
        
        print(f"🔗 Contributor label found: {'✅' if contributor_found else '❌'}")
        print(f"👨‍💻 Developer label found: {'✅' if developer_found else '❌'}")
        
        if contributor_found:
            contrib_label = main_window.contributor_label
            print(f"📝 Contributor text: '{contrib_label.text()}'")
            print(f"💡 Contributor tooltip: '{contrib_label.toolTip()}'")
            
            # Check styling
            style = contrib_label.styleSheet()
            if "color:" in style and "text-decoration: underline" in style:
                print("✅ Contributor styling applied correctly")
            else:
                print("❌ Contributor styling may be missing")
        
        if developer_found:
            dev_label = main_window.developer_label
            print(f"📝 Developer text: '{dev_label.text()}'")
            print(f"💡 Developer tooltip: '{dev_label.toolTip()}'")
        
        # Check if methods exist
        contributor_method = hasattr(main_window, 'open_contributor_github')
        developer_method = hasattr(main_window, 'open_developer_website')
        
        print(f"🔧 Contributor method exists: {'✅' if contributor_method else '❌'}")
        print(f"🔧 Developer method exists: {'✅' if developer_method else '❌'}")
        
        # Test status updates to see layout
        print("\n🔄 Testing status layout...")
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        main_window.status_label.setText(f"Ready - Test time: {timestamp}")
        print("✅ Status updated to show layout")
        
        # Create test message
        msg = QMessageBox()
        msg.setWindowTitle("Contributor Test")
        msg.setText("Contributor Link Test Completed!\n\n"
                   "Visual verification:\n"
                   "1. Check bottom of window for status bar\n"
                   "2. Status message should be on the LEFT\n"
                   "3. 'Contributor' link should be on the RIGHT (green color)\n"
                   "4. ' | ' separator between Contributor and Developer\n"
                   "5. 'Developed by Bibek' should be on the FAR RIGHT (blue color)\n\n"
                   "Test clicking both links:\n"
                   "• Contributor → Opens GitHub repository\n"
                   "• Developer → Opens personal website\n\n"
                   "Click OK when finished testing...")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Set icon for message box
        icon_path = "icon.png"
        try:
            from PySide6.QtGui import QIcon
            import os
            if os.path.exists(icon_path):
                msg.setWindowIcon(QIcon(icon_path))
        except:
            pass
        
        # Show message and wait for user
        msg.exec()
        
        # Test the click functionality programmatically
        print("\n🔗 Testing link functionality...")
        try:
            if contributor_method:
                main_window.open_contributor_github(None)
                print("✅ Contributor GitHub link method executed")
        except Exception as e:
            print(f"❌ Error testing contributor link: {e}")
        
        try:
            if developer_method:
                main_window.open_developer_website(None)
                print("✅ Developer website link method executed")
        except Exception as e:
            print(f"❌ Error testing developer link: {e}")
        
        # Close the window
        main_window.close()
        print("✅ Test window closed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🎯 Contributor Link Addition Test")
    print("Testing the new GitHub repository link")
    print()
    
    success = test_contributor_functionality()
    
    print("\n" + "=" * 40)
    if success:
        print("✅ Contributor test completed successfully!")
        print("📊 Expected Results:")
        print("  • Two clickable links in bottom-right")
        print("  • 'Contributor' (green) → GitHub repository")
        print("  • 'Developed by Bibek' (blue) → Personal website")
        print("  • Visual separator ' | ' between links")
        print("  • Both links have hover effects")
        print("  • Both links have proper tooltips")
    else:
        print("❌ Contributor test failed!")
    
    print("\n🎉 Test completed!")

if __name__ == '__main__':
    main()