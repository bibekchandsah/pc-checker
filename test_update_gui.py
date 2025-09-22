#!/usr/bin/env python3
"""
Test script to verify update system error handling
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PySide6.QtCore import QThread

# Add current directory to path to import update_manager
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from update_manager import UpdateChecker

class UpdateTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update System Test")
        self.setGeometry(300, 300, 600, 400)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create test button
        self.test_button = QPushButton("Test Update Check")
        self.test_button.clicked.connect(self.test_update_check)
        layout.addWidget(self.test_button)
        
        # Create output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        self.update_checker = None
    
    def test_update_check(self):
        """Test the update checking with current network conditions"""
        self.output_text.append("Testing update check...")
        self.test_button.setEnabled(False)
        
        # Create update checker (using a test repo that doesn't exist to trigger different scenarios)
        self.update_checker = UpdateChecker("1.0.0", "nonexistent/repo")
        
        # Connect signals
        self.update_checker.update_available.connect(self.on_update_available)
        self.update_checker.update_not_available.connect(self.on_update_not_available)
        self.update_checker.error_occurred.connect(self.on_error_occurred)
        
        # Start the check
        self.update_checker.start()
    
    def on_update_available(self, update_info):
        self.output_text.append(f"✅ Update available: {update_info}")
        self.test_button.setEnabled(True)
    
    def on_update_not_available(self):
        self.output_text.append("ℹ️ No update available")
        self.test_button.setEnabled(True)
    
    def on_error_occurred(self, error_message):
        self.output_text.append(f"❌ Error: {error_message}")
        self.test_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = UpdateTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()