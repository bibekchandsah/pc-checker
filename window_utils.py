"""
Window Utilities Module
Provides common window management functions for the laptop testing application
"""

import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


def set_window_icon_and_center(window, icon_filename="icon.png"):
    """
    Set window icon and center the window on screen
    
    Args:
        window: QMainWindow or QWidget instance
        icon_filename: Name of the icon file (default: "icon.png")
    """
    # Set window icon
    icon_path = os.path.join(os.path.dirname(__file__), icon_filename)
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    
    # Center the window on screen
    center_window(window)


def center_window(window):
    """
    Center a window on the screen
    
    Args:
        window: QMainWindow or QWidget instance
    """
    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    window_geometry = window.frameGeometry()
    center_point = screen_geometry.center()
    window_geometry.moveCenter(center_point)
    window.move(window_geometry.topLeft())


def set_window_icon(window, icon_filename="icon.png"):
    """
    Set window icon
    
    Args:
        window: QMainWindow or QWidget instance  
        icon_filename: Name of the icon file (default: "icon.png")
    """
    icon_path = os.path.join(os.path.dirname(__file__), icon_filename)
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    else:
        print(f"Warning: Icon file '{icon_filename}' not found at {icon_path}")


# For backward compatibility and convenience
def setup_window(window, title=None, size=None, icon_filename="icon.png"):
    """
    Complete window setup with title, size, icon, and centering
    
    Args:
        window: QMainWindow or QWidget instance
        title: Window title (optional)
        size: Tuple of (width, height) for window size (optional)
        icon_filename: Name of the icon file (default: "icon.png")
    """
    if title:
        window.setWindowTitle(title)
    
    if size:
        width, height = size
        window.resize(width, height)
    
    set_window_icon_and_center(window, icon_filename)