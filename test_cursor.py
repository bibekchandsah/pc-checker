#!/usr/bin/env python3

"""
Quick cursor test to verify pointing hand cursor works
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class CursorTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor Test")
        self.setGeometry(100, 100, 300, 200)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Test label with pointing hand cursor
        test_label = QLabel("Hover over me - should show pointing hand")
        test_label.setStyleSheet("""
            QLabel {
                color: blue;
                text-decoration: underline;
                padding: 10px;
                border: 1px solid gray;
            }
        """)
        test_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        layout.addWidget(test_label)
        
        # Normal label for comparison
        normal_label = QLabel("Normal label - should show normal cursor")
        normal_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                border: 1px solid gray;
            }
        """)
        
        layout.addWidget(normal_label)

def main():
    app = QApplication(sys.argv)
    window = CursorTestWindow()
    window.show()
    
    print("Hover over the blue underlined label - it should show a pointing hand cursor")
    print("Close the window to end the test")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()