"""
Camera Test Module
Implements camera testing with integrated preview window
"""

import sys
import threading
import subprocess
import time
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QPushButton, QTextEdit, QGroupBox, QApplication)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QImage, QPixmap

# Try to import OpenCV, but make it optional
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None

class CameraWorker(QThread):
    """Worker thread for camera operations"""
    frame_ready = Signal(object)
    status_update = Signal(str)
    camera_info_ready = Signal(dict)  # New signal for camera info
    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.running = False
        self.flip_horizontal = True  # Enable horizontal flip by default
        
    def set_flip_horizontal(self, flip):
        """Set horizontal flip state"""
        self.flip_horizontal = flip
        
    def run(self):
        """Main camera capture loop"""
        try:
            if not OPENCV_AVAILABLE:
                self.status_update.emit("❌ OpenCV not available - install opencv-python")
                return
                
            # Try to open camera with timeout
            self.status_update.emit("🔄 Initializing camera...")
            self.camera = cv2.VideoCapture(0)
            
            # Set a timeout for camera initialization
            start_time = time.time()
            timeout = 5  # 5 seconds timeout
            
            while not self.camera.isOpened() and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            if not self.camera.isOpened():
                self.status_update.emit("❌ Failed to open camera (timeout)")
                return
            
            # Set camera properties for better performance
            self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.status_update.emit("✅ Camera opened successfully")
            self.running = True
            
            # Emit camera info once camera is ready
            self.emit_camera_info()
            
            frame_count = 0
            while self.running:
                ret, frame = self.camera.read()
                if ret:
                    # Flip frame horizontally if enabled (mirror effect)
                    if self.flip_horizontal:
                        frame = cv2.flip(frame, 1)
                    
                    # Convert BGR to RGB
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.frame_ready.emit(rgb_frame)
                    frame_count += 1
                    
                    # Update camera info every 60 frames
                    if frame_count % 60 == 0:
                        self.emit_camera_info()
                else:
                    self.status_update.emit("❌ Failed to read frame")
                    break
                    
                self.msleep(33)  # ~30 FPS
                
                # Update status every 30 frames
                if frame_count % 30 == 0:
                    self.status_update.emit(f"📹 Recording... ({frame_count} frames)")
                
        except Exception as e:
            self.status_update.emit(f"❌ Camera error: {str(e)}")
        finally:
            if self.camera and self.camera.isOpened():
                self.camera.release()
            self.status_update.emit("📷 Camera released")
    
    def emit_camera_info(self):
        """Emit camera information"""
        try:
            if self.camera and self.camera.isOpened():
                camera_info = {
                    'active': True,
                    'width': int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    'height': int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    'fps': self.camera.get(cv2.CAP_PROP_FPS),
                    'backend': self.camera.getBackendName(),
                    'brightness': self.camera.get(cv2.CAP_PROP_BRIGHTNESS),
                    'contrast': self.camera.get(cv2.CAP_PROP_CONTRAST),
                    'saturation': self.camera.get(cv2.CAP_PROP_SATURATION),
                    'flip_horizontal': self.flip_horizontal
                }
                self.camera_info_ready.emit(camera_info)
        except Exception as e:
            self.status_update.emit(f"❌ Camera info error: {str(e)}")
    
    def stop(self):
        """Stop camera capture"""
        self.running = False
        self.wait()

class CameraTestWindow(QMainWindow):
    """Camera test window with integrated preview"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera_worker = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("📷 Camera Test")
        self.setGeometry(100, 100, 890, 730)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("📷 Camera Test")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Content layout (horizontal)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left side - Camera preview
        preview_group = QGroupBox("Camera Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.camera_label = QLabel("Camera preview will appear here")
        self.camera_label.setMinimumSize(480, 360)
        self.camera_label.setStyleSheet("""
            QLabel {
                border: 2px solid #333;
                background-color: #f0f0f0;
                text-align: center;
                font-size: 14px;
            }
        """)
        self.camera_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.camera_label)
        
        # Camera controls
        camera_controls_layout = QHBoxLayout()
        
        self.start_camera_btn = QPushButton("🎥 Start Camera")
        self.start_camera_btn.clicked.connect(self.start_camera)
        camera_controls_layout.addWidget(self.start_camera_btn)
        
        self.stop_camera_btn = QPushButton("⏹️ Stop Camera")
        self.stop_camera_btn.clicked.connect(self.stop_camera)
        self.stop_camera_btn.setEnabled(False)
        camera_controls_layout.addWidget(self.stop_camera_btn)
        
        # Add flip camera button
        self.flip_camera_btn = QPushButton("🔄 Flip Camera")
        self.flip_camera_btn.clicked.connect(self.toggle_flip)
        self.flip_camera_btn.setEnabled(False)
        self.flip_camera_btn.setToolTip("Toggle horizontal flip (mirror effect)")
        camera_controls_layout.addWidget(self.flip_camera_btn)
        
        preview_layout.addLayout(camera_controls_layout)
        content_layout.addWidget(preview_group)
        
        # Right side - Controls and info
        controls_group = QGroupBox("Camera Controls & Debug")
        controls_layout = QVBoxLayout(controls_group)
        
        # Status display
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: #212121;")
        controls_layout.addWidget(self.status_label)
        
        # Manual camera app button
        self.manual_camera_btn = QPushButton("📱 Open Camera App")
        self.manual_camera_btn.clicked.connect(self.open_camera_app)
        controls_layout.addWidget(self.manual_camera_btn)
        
        # Debug camera settings button
        self.debug_camera_btn = QPushButton("🔧 Debug Camera Settings")
        self.debug_camera_btn.clicked.connect(self.open_camera_settings)
        controls_layout.addWidget(self.debug_camera_btn)
        
        # Camera info
        info_label = QLabel("Camera Information:")
        info_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        controls_layout.addWidget(info_label)
        
        self.camera_info = QTextEdit()
        self.camera_info.setMaximumHeight(200)
        self.camera_info.setPlainText("Click 'Start Camera' to get camera information...")
        controls_layout.addWidget(self.camera_info)
        
        # Instructions
        instructions_label = QLabel("Instructions:")
        instructions_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        controls_layout.addWidget(instructions_label)
        
        instructions_text = QLabel("""
• Remove the camera slider cover if present
• Click 'Start Camera' to begin camera preview
• Use 'Flip Camera' to toggle horizontal mirror effect
• Verify that video appears clearly in the preview
• Test different lighting conditions
• Use 'Open Camera App' for system camera app
• Use 'Debug Camera Settings' for troubleshooting
• Open 'Integrated Camera' and click disable & enable it again if issue occurs
        """)
        instructions_text.setWordWrap(True)
        instructions_text.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 5px;")
        controls_layout.addWidget(instructions_text)
        
        controls_layout.addStretch()
        content_layout.addWidget(controls_group)
        
        # Close button
        close_btn = QPushButton("Close Camera Test")
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)
        
    def start_camera(self):
        """Start camera preview"""
        try:
            # Check if OpenCV is available first
            if not OPENCV_AVAILABLE:
                self.update_status("❌ OpenCV not available - install: pip install opencv-python")
                self.camera_info.setPlainText("Error: OpenCV not installed\n\nTo fix this:\n1. Open terminal/command prompt\n2. Run: pip install opencv-python\n3. Restart the application")
                return
            
            if self.camera_worker is None or not self.camera_worker.isRunning():
                self.update_status("🔄 Initializing camera...")
                self.start_camera_btn.setEnabled(False)
                self.stop_camera_btn.setEnabled(True)
                self.flip_camera_btn.setEnabled(True)
                
                # Create and start camera worker
                self.camera_worker = CameraWorker()
                self.camera_worker.frame_ready.connect(self.update_frame)
                self.camera_worker.status_update.connect(self.update_status)
                self.camera_worker.camera_info_ready.connect(self.update_camera_info)
                self.camera_worker.start()
                
        except Exception as e:
            self.update_status(f"❌ Error starting camera: {str(e)}")
            self.start_camera_btn.setEnabled(True)
            self.stop_camera_btn.setEnabled(False)
            self.flip_camera_btn.setEnabled(False)
    
    def stop_camera(self):
        """Stop camera preview"""
        try:
            if self.camera_worker and self.camera_worker.isRunning():
                self.camera_worker.stop()
                
            self.start_camera_btn.setEnabled(True)
            self.stop_camera_btn.setEnabled(False)
            self.flip_camera_btn.setEnabled(False)
            self.camera_label.setText("Camera preview stopped")
            self.update_status("⏹️ Camera stopped")
            
            # Reset camera info
            self.camera_info.setPlainText("Click 'Start Camera' to get camera information...")
            
        except Exception as e:
            self.update_status(f"❌ Error stopping camera: {str(e)}")
    
    def update_frame(self, frame):
        """Update camera preview with new frame"""
        try:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Scale image to fit label
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.camera_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.update_status(f"❌ Frame update error: {str(e)}")
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(f"Status: {status}")
    
    def toggle_flip(self):
        """Toggle horizontal flip of camera"""
        if self.camera_worker and self.camera_worker.isRunning():
            current_flip = self.camera_worker.flip_horizontal
            new_flip = not current_flip
            self.camera_worker.set_flip_horizontal(new_flip)
            
            if new_flip:
                self.flip_camera_btn.setText("🔄 Flip: ON")
                self.update_status("🔄 Camera flipped horizontally (mirror mode)")
            else:
                self.flip_camera_btn.setText("🔄 Flip: OFF")
                self.update_status("🔄 Camera flip disabled (normal mode)")
    
    def update_camera_info(self, camera_info):
        """Update camera information display with live data"""
        try:
            if camera_info.get('active', False):
                info_text = "Camera Information:\n\n"
                info_text += f"Status: ✅ Active\n"
                info_text += f"Resolution: {camera_info['width']} x {camera_info['height']}\n"
                info_text += f"FPS: {camera_info['fps']:.1f}\n"
                info_text += f"Backend: {camera_info['backend']}\n"
                
                info_text += f"\nCamera Settings:\n"
                info_text += f"Brightness: {camera_info['brightness']:.2f}\n"
                info_text += f"Contrast: {camera_info['contrast']:.2f}\n"
                info_text += f"Saturation: {camera_info['saturation']:.2f}\n"
                
                info_text += f"\nDisplay Options:\n"
                flip_status = "ON (Mirror)" if camera_info['flip_horizontal'] else "OFF (Normal)"
                info_text += f"Horizontal Flip: {flip_status}\n"
                
                info_text += f"\nLast Updated: {datetime.now().strftime('%H:%M:%S')}\n"
                
                self.camera_info.setPlainText(info_text)
                
                # Update flip button text
                if camera_info['flip_horizontal']:
                    self.flip_camera_btn.setText("🔄 Flip: ON")
                else:
                    self.flip_camera_btn.setText("🔄 Flip: OFF")
            else:
                self.camera_info.setPlainText("Camera not active\n")
                
        except Exception as e:
            self.camera_info.setPlainText(f"Error updating camera info: {str(e)}")
    
    def open_camera_app(self):
        """Open the system camera application"""
        try:
            if sys.platform == "win32":
                # Windows Camera app
                subprocess.run(['start', 'microsoft.windows.camera:'], shell=True)
                self.update_status("📱 Camera app launched")
            elif sys.platform == "darwin":  # macOS
                subprocess.run(['open', '-a', 'Photo Booth'])
                self.update_status("📱 Photo Booth launched")
            else:  # Linux
                subprocess.run(['cheese'])
                self.update_status("📱 Cheese camera app launched")
                
        except Exception as e:
            self.update_status(f"❌ Failed to open camera app: {str(e)}")
    
    def open_camera_settings(self):
        """Open camera settings in Windows Settings"""
        try:
            if sys.platform == "win32":
                # Open Windows Settings -> Bluetooth & devices -> Cameras
                subprocess.run(['start', 'ms-settings:camera'], shell=True)
                self.update_status("🔧 Camera settings opened")
            elif sys.platform == "darwin":  # macOS
                subprocess.run(['open', '-b', 'com.apple.preference.security'])
                self.update_status("🔧 Security preferences opened")
            else:  # Linux
                # Try to open system settings (varies by desktop environment)
                try:
                    subprocess.run(['gnome-control-center', 'camera'])
                except:
                    subprocess.run(['systemsettings5', 'camera'])
                self.update_status("🔧 System settings opened")
                
        except Exception as e:
            self.update_status(f"❌ Failed to open camera settings: {str(e)}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.stop_camera()
        event.accept()

class CameraTest:
    """Camera test class that integrates with the main testing system"""
    
    def __init__(self):
        self.window = None
    
    def run_test(self, callback=None):
        """Run camera test - opens camera test window"""
        results = {
            'test_name': 'Camera Test',
            'start_time': datetime.now(),
            'status': 'Running',
            'progress': 50,
            'window_opened': False,
            'errors': []
        }
        
        try:
            # Check if we can import required modules
            if not OPENCV_AVAILABLE:
                results['errors'].append("OpenCV not available - run: pip install opencv-python")
                results['status'] = 'Warning'
                results['progress'] = 100
                results['end_time'] = datetime.now()
                if callback:
                    callback(results)
                return results
            
            # Create camera test window directly (synchronous but fast)
            self.window = CameraTestWindow()
            self.window.show()
            
            results['window_opened'] = True
            results['status'] = 'Completed'
            results['progress'] = 100
            results['end_time'] = datetime.now()
            
            if callback:
                callback(results)
                
        except Exception as e:
            results['errors'].append(f"Failed to create camera test window: {str(e)}")
            results['status'] = 'Error'
            results['progress'] = 100
            results['end_time'] = datetime.now()
            if callback:
                callback(results)
        
        return results