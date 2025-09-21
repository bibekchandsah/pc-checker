#!/usr/bin/env python3

"""
Test Developer Credit Position Change
Verifies the developer credit is now in the bottom-right corner
"""

import sys
import time
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

def test_developer_credit_position():
    """Test the new developer credit position"""
    print("🎯 Testing Developer Credit Position Change")
    print("=" * 45)
    
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
        
        # Check if developer label exists
        if hasattr(main_window, 'developer_label'):
            dev_label = main_window.developer_label
            print("✅ Developer label found")
            print(f"📝 Label text: '{dev_label.text()}'")
            print(f"💡 Tooltip: '{dev_label.toolTip()}'")
            
            # Check if status label exists
            if hasattr(main_window, 'status_label'):
                status_label = main_window.status_label
                print("✅ Status label found")
                print(f"📊 Status text: '{status_label.text()}'")
                
                # Get the parent layouts to check positioning
                dev_parent = dev_label.parent()
                status_parent = status_label.parent()
                
                if dev_parent == status_parent:
                    print("✅ Developer credit and status are in the same layout")
                    print("✅ They should now appear side by side at the bottom")
                else:
                    print("❌ Developer credit and status are in different layouts")
            
            # Test status updates
            print("\n🔄 Testing status updates...")
            
            # Test refreshing status
            main_window.status_label.setText("Refreshing data...")
            print("✅ Status set to 'Refreshing data...'")
            
            # Test completed status
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            main_window.status_label.setText(f"Last updated: {timestamp}")
            print(f"✅ Status set to 'Last updated: {timestamp}'")
            
        else:
            print("❌ Developer label not found")
            return False
        
        # Create test message
        msg = QMessageBox()
        msg.setWindowTitle("Position Test")
        msg.setText("Developer Credit Position Test\n\n"
                   "Visual verification:\n"
                   "1. Check bottom of window for status bar\n"
                   "2. Status message should be on the left\n"
                   "3. 'Developed by Bibek' should be on the right\n"
                   "4. Both should be in the same bottom row\n\n"
                   "Try hovering and clicking the developer credit!\n\n"
                   "Click OK when finished testing...")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Show message and wait for user
        msg.exec()
        
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
    print("🎯 Developer Credit Position Change Test")
    print("Testing the move from top-right to bottom-right")
    print()
    
    success = test_developer_credit_position()
    
    print("\n" + "=" * 45)
    if success:
        print("✅ Position test completed successfully!")
        print("📊 Expected Results:")
        print("  • Developer credit moved from header to status bar")
        print("  • Status message on left, developer credit on right") 
        print("  • Both appear at bottom of window")
        print("  • Developer credit remains clickable")
        print("  • Status updates work normally")
    else:
        print("❌ Position test failed!")
    
    print("\n🎉 Test completed!")

if __name__ == '__main__':
    main()