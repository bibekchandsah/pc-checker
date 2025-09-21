# Laptop Testing Program

A comprehensive laptop testing application built with Python and PySide6 that provides detailed hardware and OS information along with system testing capabilities.

## ✅ Latest Updates (v1.1)

**Fixed Hardware Details Display Issue**: 
- Tree widget now properly shows Property-Value columns
- Hardware details are fully visible with proper formatting
- Column widths automatically adjusted for better readability
- All hardware specifications now display correctly

## Features

### 🖥️ System Overview
- Real-time system monitoring (CPU, Memory, Disk usage)
- System summary with hostname, OS, processor, memory info
- Uptime and system temperature monitoring
- Auto-refresh functionality with 30-second intervals

### 🔧 Hardware Details
- **CPU Information**: Name, cores, frequency, cache, temperature, per-core usage
- **Memory Information**: Total/available memory, swap usage, memory slot details
- **Storage Information**: Disk partitions, physical disks, I/O statistics
- **GPU Information**: Graphics cards with NVIDIA GPU support via GPUtil
- **Network Information**: Network interfaces, IP addresses, I/O statistics
- **System Information**: BIOS, motherboard, manufacturer details
- **Battery Information**: Battery status and power information

### 💻 Operating System Details
- Complete OS information (Windows-focused with WMI support)
- Installed software list from Windows registry
- System services and drivers
- Startup programs
- Users and groups information
- Network configuration details
- Environment variables and PATH entries

### 🧪 System Tests
- **CPU Stress Test**: Multi-core stress testing with temperature monitoring
- **Memory Test**: RAM integrity testing with configurable size
- **Disk Speed Test**: Read/write speed benchmarking
- **Network Speed Test**: Internet speed testing using speedtest-cli
- **System Stability Test**: Comprehensive stability monitoring
- **Keyboard Test**: Interactive keyboard testing with glassmorphism UI and key highlighting
- **Camera Test**: Integrated camera testing with live preview and horizontal flip functionality
- **Microphone Test**: Audio capture testing with real-time waveform visualization

## Requirements

### Python Packages
```
PySide6==6.9.2
psutil==6.0.0
py-cpuinfo==9.0.0
GPUtil==1.4.0
wmi==1.5.1 (Windows only)
requests==2.31.0
speedtest-cli==2.1.3
opencv-python (for camera test)
pyaudio (for microphone test)
matplotlib (for microphone waveform)
numpy (for audio processing)
scipy (optional for advanced audio features)
```

### System Requirements
- Python 3.8+
- Windows 10/11 (optimal support with WMI)
- Linux support available (limited features without WMI)

## Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have these files:
   # - script.py (main application)
   # - hardware_info.py (hardware information module)
   # - os_info.py (OS information module) 
   # - system_tests.py (testing module)
   # - requirements.txt (dependencies)
   # - test_modules.py (test script)
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run module tests (optional)**
   ```bash
   python test_modules.py
   ```

4. **Launch the application**
   ```bash
   python script.py
   ```

## Usage

### Main Interface
The application features a tabbed interface with four main sections:

1. **System Overview Tab**
   - Quick system summary
   - Real-time monitoring widgets
   - Detailed system information text area

2. **Hardware Details Tab**
   - Expandable tree view of all hardware components
   - Detailed specifications for CPU, memory, storage, GPU, etc.

3. **OS Details Tab**
   - Operating system configuration
   - Network settings
   - Environment variables

4. **System Tests Tab**
   - Test execution controls
   - Configurable test parameters
   - Real-time progress monitoring
   - Test results display

### Running Tests

#### CPU Stress Test
- Duration: 10-300 seconds (configurable)
- Multi-core stress testing
- Temperature monitoring (if available)
- Usage statistics

#### Memory Test
- Size: 10-1000 MB (configurable)
- Memory allocation and integrity testing
- Error detection

#### Disk Speed Test
- File size: 10-1000 MB (configurable)
- Sequential read/write speed testing
- Temporary file creation and cleanup

#### Network Speed Test
- Internet connectivity testing
- Download/upload speed measurement
- Ping latency testing
- Server information

### Auto-Refresh
- Automatic data refresh every 30 seconds
- Can be disabled via checkbox
- Manual refresh button available

## Technical Details

### Architecture
- **Hardware Module**: Uses `psutil`, `py-cpuinfo`, `GPUtil`, and `wmi` for comprehensive hardware detection
- **OS Module**: Windows registry access and WMI queries for detailed OS information
- **Testing Module**: Multi-threaded testing with callback-based progress reporting
- **GUI Module**: PySide6-based interface with worker threads for non-blocking operations

### Platform Support
- **Windows**: Full feature support with WMI integration
- **Linux**: Basic hardware detection (WMI features unavailable)
- **macOS**: Limited testing, basic psutil functionality

### Performance Considerations
- Background data collection to prevent UI freezing
- Efficient memory usage with selective data loading
- Threaded test execution for responsive interface

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Install missing packages
   pip install -r requirements.txt
   ```

2. **WMI Not Available (Non-Windows)**
   - Some advanced features will be disabled
   - Basic hardware detection still functional

3. **Permission Errors**
   - Run as administrator for full hardware access
   - Some temperature sensors require elevated privileges

4. **Network Test Failures**
   - Check internet connectivity
   - Firewall may block speedtest-cli

### Error Messages
- Check the test_modules.py output for specific module errors
- GUI errors are displayed in the status bar
- Test failures show detailed error messages

## Development

### File Structure
```
├── script.py              # Main application GUI
├── hardware_info.py       # Hardware detection module
├── os_info.py            # OS information module
├── system_tests.py       # Testing functionality
├── requirements.txt      # Python dependencies
├── test_modules.py       # Module testing script
└── README.md            # This file
```

### Adding New Features
1. Hardware detection: Extend `HardwareInfo` class
2. OS information: Extend `OSInfo` class  
3. New tests: Add to `SystemTests` class
4. GUI components: Modify tabs in `script.py`

### Contributing
- Follow PEP 8 style guidelines
- Add error handling for new features
- Test on multiple platforms when possible
- Update requirements.txt for new dependencies

## License

This project is open source and available under the MIT License.

## Version History

- **v1.0**: Initial release with full hardware/OS detection and testing capabilities

## Contact

For issues, suggestions, or contributions, please create an issue in the project repository.

---

**Note**: This application provides read-only system information and non-destructive testing. All tests are designed to be safe for normal computer operation.