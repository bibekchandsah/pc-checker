"""
Microphone Test Module
Implements microphone testing with visual waveform display
"""

import sys
import threading
import subprocess
import time
import os
import numpy as np
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QPushButton, QTextEdit, QGroupBox, QApplication,
                              QSlider, QProgressBar)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Try to import audio libraries
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    pyaudio = None

try:
    import scipy.signal
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    scipy = None

class AudioWorker(QThread):
    """Worker thread for audio capture and processing"""
    audio_data_ready = Signal(object)
    volume_level_ready = Signal(float)
    status_update = Signal(str)
    audio_info_ready = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.audio = None
        self.stream = None
        self.running = False
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
        
    def run(self):
        """Main audio capture loop"""
        try:
            if not PYAUDIO_AVAILABLE:
                self.status_update.emit("❌ PyAudio not available - install pyaudio")
                return
                
            # Initialize PyAudio
            self.status_update.emit("🔄 Initializing microphone...")
            self.audio = pyaudio.PyAudio()
            
            # Try to open microphone stream
            try:
                self.stream = self.audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=self.chunk_size
                )
                
                self.status_update.emit("✅ Microphone opened successfully")
                self.running = True
                
                # Emit microphone info
                self.emit_audio_info()
                
                while self.running:
                    try:
                        # Read audio data
                        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                        
                        # Convert to numpy array
                        audio_data = np.frombuffer(data, dtype=np.int16)
                        
                        # Calculate volume level (RMS) with safety checks
                        try:
                            if len(audio_data) > 0:
                                # Use float64 for calculations to avoid overflow
                                audio_float = audio_data.astype(np.float64)
                                mean_square = np.mean(audio_float**2)
                                
                                # Check for valid values
                                if np.isfinite(mean_square) and mean_square >= 0:
                                    volume = np.sqrt(mean_square)
                                    # Clamp volume to reasonable range
                                    volume = max(0, min(volume, 32768))
                                    
                                    if volume > 0:
                                        volume_db = 20 * np.log10(volume / 32768 + 1e-10)  # Add small epsilon
                                        volume_db = max(-60, min(0, volume_db))  # Clamp to -60 to 0 dB
                                    else:
                                        volume_db = -60
                                        
                                    # Normalize volume for display (0-100)
                                    volume_normalized = max(0, min(100, (volume_db + 60) * 100 / 60))
                                else:
                                    volume_normalized = 0
                            else:
                                volume_normalized = 0
                        except Exception as vol_e:
                            self.status_update.emit(f"Volume calculation error: {str(vol_e)}")
                            volume_normalized = 0
                        
                        # Emit data (limit frequency to prevent UI freezing)
                        self.audio_data_ready.emit(audio_data)
                        self.volume_level_ready.emit(volume_normalized)
                        
                        # Add small delay to prevent overwhelming the UI
                        time.sleep(0.01)  # 10ms delay
                        
                    except Exception as e:
                        self.status_update.emit(f"❌ Audio read error: {str(e)}")
                        break
                        
            except Exception as e:
                self.status_update.emit(f"❌ Failed to open microphone: {str(e)}")
                
        except Exception as e:
            self.status_update.emit(f"❌ Audio initialization error: {str(e)}")
        finally:
            self.cleanup()
    
    def emit_audio_info(self):
        """Emit microphone information"""
        try:
            if self.audio:
                # Get default input device info
                default_device = self.audio.get_default_input_device_info()
                
                audio_info = {
                    'active': True,
                    'sample_rate': self.sample_rate,
                    'channels': self.channels,
                    'chunk_size': self.chunk_size,
                    'device_name': default_device.get('name', 'Unknown'),
                    'max_input_channels': default_device.get('maxInputChannels', 0),
                    'default_sample_rate': default_device.get('defaultSampleRate', 0)
                }
                self.audio_info_ready.emit(audio_info)
        except Exception as e:
            self.status_update.emit(f"❌ Audio info error: {str(e)}")
    
    def cleanup(self):
        """Clean up audio resources"""
        try:
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except Exception as e:
                    print(f"Error closing stream: {e}")
                self.stream = None
                
            if self.audio:
                try:
                    self.audio.terminate()
                except Exception as e:
                    print(f"Error terminating audio: {e}")
                self.audio = None
                
            self.status_update.emit("🎤 Microphone released")
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def stop(self):
        """Stop audio capture"""
        self.running = False
        # Give the thread time to finish
        if self.isRunning():
            if not self.wait(3000):  # Wait up to 3 seconds
                print("Warning: Audio thread did not stop gracefully")
                try:
                    self.terminate()  # Force terminate if needed
                except:
                    pass

class WaveformWidget(FigureCanvas):
    """Custom widget for displaying audio waveform"""
    
    def __init__(self, parent=None, width=6, height=3, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi, facecolor='#2d2d2d')
        super().__init__(self.figure)
        self.setParent(parent)
        
        # Create subplot
        self.axes = self.figure.add_subplot(111, facecolor='#1e1e1e')
        self.axes.set_xlim(0, 1024)
        self.axes.set_ylim(-32768, 32767)
        self.axes.set_xlabel('Sample', color='white')
        self.axes.set_ylabel('Amplitude', color='white')
        self.axes.set_title('Microphone Waveform', color='white', fontsize=12)
        self.axes.tick_params(colors='white')
        self.axes.grid(True, alpha=0.3)
        
        # Initialize empty line plot
        self.line, = self.axes.plot([], [], color='#00ff00', linewidth=1)
        
        # Set dark theme
        self.figure.patch.set_facecolor('#2d2d2d')
        
        # Add update throttling
        self.last_update_time = 0
        self.update_interval = 0.05  # Update every 50ms max
        
    def update_waveform(self, audio_data):
        """Update the waveform display with new audio data"""
        try:
            # Throttle updates to prevent UI freezing
            current_time = time.time()
            if current_time - self.last_update_time < self.update_interval:
                return
            
            self.last_update_time = current_time
            
            # Validate data
            if audio_data is None or len(audio_data) == 0:
                return
            
            # Downsample if data is too large to improve performance
            if len(audio_data) > 1024:
                step = len(audio_data) // 1024
                audio_data = audio_data[::step][:1024]
            
            x = np.arange(len(audio_data))
            self.line.set_data(x, audio_data)
            
            # Auto-scale y-axis based on data with safety checks
            if len(audio_data) > 0:
                try:
                    min_val = np.min(audio_data)
                    max_val = np.max(audio_data)
                    
                    if np.isfinite(min_val) and np.isfinite(max_val):
                        abs_max = max(abs(min_val), abs(max_val))
                        if abs_max > 0:
                            self.axes.set_ylim(-abs_max * 1.1, abs_max * 1.1)
                        else:
                            self.axes.set_ylim(-1000, 1000)  # Default range
                    else:
                        self.axes.set_ylim(-32768, 32767)  # Default range
                except Exception as scale_e:
                    print(f"Y-axis scaling error: {scale_e}")
                    self.axes.set_ylim(-32768, 32767)
            
            # Use blit for faster updates
            self.draw_idle()
            
        except Exception as e:
            print(f"Waveform update error: {e}")

class MicrophoneTestWindow(QMainWindow):
    """Microphone test window with waveform visualization"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.audio_worker = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🎤 Microphone Test")
        self.setGeometry(100, 100, 1180, 720)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Center the window on screen
        self.center_window()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("🎤 Microphone Test")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Content layout (horizontal)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left side - Waveform display
        waveform_group = QGroupBox("Audio Waveform Visualization")
        waveform_layout = QVBoxLayout(waveform_group)
        
        # Waveform canvas
        self.waveform_widget = WaveformWidget(self, width=8, height=4)
        waveform_layout.addWidget(self.waveform_widget)
        
        # Volume level display
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume Level:"))
        
        self.volume_bar = QProgressBar()
        self.volume_bar.setRange(0, 100)
        self.volume_bar.setValue(0)
        self.volume_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #333;
                border-radius: 5px;
                text-align: center;
                background-color: #1e1e1e;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff00, stop:0.7 #ffff00, stop:1 #ff0000);
                border-radius: 3px;
            }
        """)
        volume_layout.addWidget(self.volume_bar)
        
        self.volume_label = QLabel("0%")
        self.volume_label.setMinimumWidth(40)
        volume_layout.addWidget(self.volume_label)
        
        waveform_layout.addLayout(volume_layout)
        
        # Audio controls
        audio_controls_layout = QHBoxLayout()
        
        self.start_audio_btn = QPushButton("🎤 Start Recording")
        self.start_audio_btn.clicked.connect(self.start_audio)
        audio_controls_layout.addWidget(self.start_audio_btn)
        
        self.stop_audio_btn = QPushButton("⏹️ Stop Recording")
        self.stop_audio_btn.clicked.connect(self.stop_audio)
        self.stop_audio_btn.setEnabled(False)
        audio_controls_layout.addWidget(self.stop_audio_btn)
        
        # Test sound button
        self.test_sound_btn = QPushButton("🔊 Test System Audio")
        self.test_sound_btn.clicked.connect(self.test_system_audio)
        audio_controls_layout.addWidget(self.test_sound_btn)
        
        waveform_layout.addLayout(audio_controls_layout)
        content_layout.addWidget(waveform_group)
        
        # Right side - Controls and info
        controls_group = QGroupBox("Microphone Controls & Info")
        controls_layout = QVBoxLayout(controls_group)
        
        # Status display
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: #212121;")
        controls_layout.addWidget(self.status_label)
        
        # Microphone settings button
        self.mic_settings_btn = QPushButton("🔧 Microphone Settings")
        self.mic_settings_btn.clicked.connect(self.open_mic_settings)
        controls_layout.addWidget(self.mic_settings_btn)
        
        # Sound settings button
        self.sound_settings_btn = QPushButton("🔊 Sound Settings")
        self.sound_settings_btn.clicked.connect(self.open_sound_settings)
        controls_layout.addWidget(self.sound_settings_btn)
        
        # Audio info
        info_label = QLabel("Microphone Information:")
        info_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        controls_layout.addWidget(info_label)
        
        self.audio_info = QTextEdit()
        self.audio_info.setMaximumHeight(200)
        self.audio_info.setPlainText("Click 'Start Recording' to get microphone information...")
        controls_layout.addWidget(self.audio_info)
        
        # Instructions
        instructions_label = QLabel("Instructions:")
        instructions_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        controls_layout.addWidget(instructions_label)
        
        instructions_text = QLabel("""
• Click 'Start Recording' to begin microphone test
• Speak or make sounds to see waveform visualization
• Check volume level bar for input sensitivity
• Use 'Test System Audio' to verify speakers
• Use settings buttons for microphone configuration
• Verify both input and output audio functionality
        """)
        instructions_text.setWordWrap(True)
        instructions_text.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 5px;")
        controls_layout.addWidget(instructions_text)
        
        controls_layout.addStretch()
        content_layout.addWidget(controls_group)
        
        # Close button
        close_btn = QPushButton("Close Microphone Test")
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)
        
    def start_audio(self):
        """Start microphone recording and visualization"""
        try:
            # Check if PyAudio is available
            if not PYAUDIO_AVAILABLE:
                self.update_status("❌ PyAudio not available - install: pip install pyaudio")
                self.audio_info.setPlainText("Error: PyAudio not installed\n\nTo fix this:\n1. Open terminal/command prompt\n2. Run: pip install pyaudio\n3. Restart the application")
                return
            
            if self.audio_worker is None or not self.audio_worker.isRunning():
                self.update_status("🔄 Initializing microphone...")
                self.start_audio_btn.setEnabled(False)
                self.stop_audio_btn.setEnabled(True)
                
                # Create and start audio worker
                self.audio_worker = AudioWorker()
                self.audio_worker.audio_data_ready.connect(self.update_waveform)
                self.audio_worker.volume_level_ready.connect(self.update_volume)
                self.audio_worker.status_update.connect(self.update_status)
                self.audio_worker.audio_info_ready.connect(self.update_audio_info)
                self.audio_worker.start()
                
        except Exception as e:
            self.update_status(f"❌ Error starting microphone: {str(e)}")
            self.start_audio_btn.setEnabled(True)
            self.stop_audio_btn.setEnabled(False)
    
    def stop_audio(self):
        """Stop microphone recording"""
        try:
            if self.audio_worker and self.audio_worker.isRunning():
                self.audio_worker.stop()
                
            self.start_audio_btn.setEnabled(True)
            self.stop_audio_btn.setEnabled(False)
            self.update_status("⏹️ Microphone stopped")
            
            # Reset displays
            self.volume_bar.setValue(0)
            self.volume_label.setText("0%")
            self.audio_info.setPlainText("Click 'Start Recording' to get microphone information...")
            
        except Exception as e:
            self.update_status(f"❌ Error stopping microphone: {str(e)}")
    
    def update_waveform(self, audio_data):
        """Update waveform visualization"""
        try:
            self.waveform_widget.update_waveform(audio_data)
        except Exception as e:
            self.update_status(f"❌ Waveform update error: {str(e)}")
    
    def update_volume(self, volume_level):
        """Update volume level display"""
        try:
            self.volume_bar.setValue(int(volume_level))
            self.volume_label.setText(f"{int(volume_level)}%")
        except Exception as e:
            self.update_status(f"❌ Volume update error: {str(e)}")
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(f"Status: {status}")
    
    def update_audio_info(self, audio_info):
        """Update microphone information display"""
        try:
            if audio_info.get('active', False):
                info_text = "Microphone Information:\n\n"
                info_text += f"Status: ✅ Active\n"
                info_text += f"Device: {audio_info['device_name']}\n"
                info_text += f"Sample Rate: {audio_info['sample_rate']} Hz\n"
                info_text += f"Channels: {audio_info['channels']}\n"
                info_text += f"Chunk Size: {audio_info['chunk_size']} samples\n"
                info_text += f"Max Input Channels: {audio_info['max_input_channels']}\n"
                info_text += f"Default Sample Rate: {audio_info['default_sample_rate']:.0f} Hz\n"
                info_text += f"\nLast Updated: {datetime.now().strftime('%H:%M:%S')}\n"
                
                self.audio_info.setPlainText(info_text)
            else:
                self.audio_info.setPlainText("Microphone not active\n")
                
        except Exception as e:
            self.audio_info.setPlainText(f"Error updating microphone info: {str(e)}")
    
    def test_system_audio(self):
        """Test system audio output"""
        try:
            self.update_status("🔊 Testing system audio...")
            
            # Generate a simple test tone
            if PYAUDIO_AVAILABLE:
                # Create a simple beep sound
                frequency = 1000  # Hz
                duration = 1  # seconds
                sample_rate = 44100
                
                # Generate sine wave
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                wave = np.sin(frequency * 2 * np.pi * t) * 0.3
                
                # Play audio
                audio = pyaudio.PyAudio()
                stream = audio.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=sample_rate,
                                  output=True)
                
                stream.write(wave.astype(np.float32).tobytes())
                stream.stop_stream()
                stream.close()
                audio.terminate()
                
                self.update_status("✅ System audio test completed")
            else:
                self.update_status("❌ Cannot test audio - PyAudio not available")
                
        except Exception as e:
            self.update_status(f"❌ Audio test error: {str(e)}")
    
    def open_mic_settings(self):
        """Open microphone settings"""
        try:
            if sys.platform == "win32":
                subprocess.run(['start', 'ms-settings:sound'], shell=True)
                self.update_status("🔧 Microphone settings opened")
            elif sys.platform == "darwin":  # macOS
                subprocess.run(['open', '-b', 'com.apple.preference.security'])
                self.update_status("🔧 Security preferences opened")
            else:  # Linux
                try:
                    subprocess.run(['gnome-control-center', 'sound'])
                except:
                    subprocess.run(['systemsettings5', 'audio'])
                self.update_status("🔧 Sound settings opened")
                
        except Exception as e:
            self.update_status(f"❌ Failed to open microphone settings: {str(e)}")
    
    def open_sound_settings(self):
        """Open sound settings"""
        try:
            if sys.platform == "win32":
                subprocess.run(['start', 'mmsys.cpl'], shell=True)
                self.update_status("🔊 Sound settings opened")
            elif sys.platform == "darwin":  # macOS
                subprocess.run(['open', '/System/Library/PreferencePanes/Sound.prefPane'])
                self.update_status("🔊 Sound preferences opened")
            else:  # Linux
                try:
                    subprocess.run(['pavucontrol'])
                except:
                    subprocess.run(['gnome-control-center', 'sound'])
                self.update_status("🔊 Sound control opened")
                
        except Exception as e:
            self.update_status(f"❌ Failed to open sound settings: {str(e)}")
    
    def center_window(self):
        """Center the window on the screen"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.stop_audio()
        event.accept()

class MicrophoneTest:
    """Microphone test class that integrates with the main testing system"""
    
    def __init__(self):
        self.window = None
    
    def run_test(self, callback=None):
        """Run microphone test - opens microphone test window"""
        results = {
            'test_name': 'Microphone Test',
            'start_time': datetime.now(),
            'status': 'Running',
            'progress': 50,
            'window_opened': False,
            'errors': []
        }
        
        try:
            # Check if we can import required modules
            if not PYAUDIO_AVAILABLE:
                results['errors'].append("PyAudio not available - run: pip install pyaudio")
                results['status'] = 'Warning'
                results['progress'] = 100
                results['end_time'] = datetime.now()
                if callback:
                    callback(results)
                return results
            
            # Create microphone test window directly
            self.window = MicrophoneTestWindow()
            self.window.show()
            
            results['window_opened'] = True
            results['status'] = 'Completed'
            results['progress'] = 100
            results['end_time'] = datetime.now()
            
            if callback:
                callback(results)
                
        except Exception as e:
            results['errors'].append(f"Failed to create microphone test window: {str(e)}")
            results['status'] = 'Error'
            results['progress'] = 100
            results['end_time'] = datetime.now()
            if callback:
                callback(results)
        
        return results