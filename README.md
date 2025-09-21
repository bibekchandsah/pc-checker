# Laptop Testing Program

A comprehensive laptop testing application built with Python and PySide6 that provides detailed hardware and OS information along with system testing capabilities and enhanced CSV reporting.

## ✅ Latest Updates (v1.1)

**Enhanced CSV Reporting with Complete System Cards**: 
- Added all 8 System Overview cards to CSV reports (CPU, RAM, ROM, Battery, Other Information, etc.)
- Complete installed software list (all entries, not just top 10)
- Comprehensive system card details matching GUI layout
- Professional CSV formatting with card-based organization
- All hardware specifications now included in reports

**Previous Updates (v1.01)**:
- Fixed hardware details display issue with proper Property-Value columns
- Improved tree widget formatting and column width adjustment
- Enhanced hardware specifications visibility

## Features

### 🖥️ System Overview
- **System Cards Layout**: 8 comprehensive information cards
  - System Summary Card (hostname, OS, processor, memory, uptime)
  - System Information Card (detailed OS configuration)
  - BIOS & Motherboard Card (firmware, hardware details)
  - CPU Information Card (processor specs, cores, frequencies)
  - RAM Information Card (memory slots, usage, swap details)
  - ROM Information Card (storage drives, partitions, disk info)
  - Battery Information Card (charge level, status, cycle count)
  - Other Information Card (sensors, cameras, TPM, chassis type)
- Real-time system monitoring with auto-refresh (30-second intervals)
- Professional dark theme with glassmorphism design elements

### 🔧 Hardware Details
- **CPU Information**: Name, cores, frequency, cache, temperature, per-core usage
- **Memory Information**: Total/available memory, swap usage, memory slot details
- **Storage Information**: Disk partitions, physical disks, I/O statistics
- **GPU Information**: Graphics cards with dedicated GPU detection and NVIDIA support
- **Network Information**: Network interfaces, IP addresses, I/O statistics
- **System Information**: BIOS, motherboard, manufacturer details
- **Battery Information**: Battery status, charge level, and power information

### 💻 Operating System Details
- Complete OS information (Windows-focused with WMI support)
- **Complete software inventory**: All installed software from Windows registry (95+ entries)
- System services and drivers
- Network configuration with detailed adapter information
- Environment variables and system paths

### 📊 Enhanced CSV Reports
- **Comprehensive System Reports**: Professional CSV generation with all system data
- **8 System Overview Cards**: All GUI cards included in CSV format
- **Complete Software List**: All installed software (not limited to top 10)
- **Detailed Hardware Specs**: CPU, RAM, ROM, GPU, network, and battery information
- **Professional Formatting**: Card-based organization matching GUI layout
- **Export Functionality**: One-click report generation with timestamp

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
distro (for Linux OS detection)
```

### System Requirements
- Python 3.8+
- Windows 10/11 (optimal support with WMI and complete CSV reporting)
- Linux support available (limited features without WMI)
- Administrator privileges recommended for full hardware access

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
   - **8 Professional System Cards**: Complete system information organized in cards
     - System Summary Card: Hostname, OS, processor, memory overview
     - System Information Card: Detailed OS configuration and architecture
     - BIOS & Motherboard Card: Firmware details and hardware information
     - CPU Information Card: Processor specifications and performance metrics
     - RAM Information Card: Memory details, slots, and usage statistics
     - ROM Information Card: Storage drives, partitions, and disk information
     - Battery Information Card: Power status, charge level, and battery health
     - Other Information Card: Sensors, cameras, TPM, and chassis information
   - Real-time monitoring widgets with professional dark theme
   - Auto-refresh functionality with 30-second intervals

2. **Hardware Details Tab**
   - Expandable tree view of all hardware components
   - Detailed specifications for CPU, memory, storage, GPU, network adapters
   - Professional formatting with Property-Value columns

3. **OS Details Tab**
   - Operating system configuration and version information
   - Complete network adapter details with IP addresses
   - **Complete Software Inventory**: All installed software (95+ entries)
   - Environment variables and system paths

4. **System Tests Tab**
   - Test execution controls with progress monitoring
   - Configurable test parameters for stress testing
   - Real-time results display and error reporting

### 📊 CSV Report Generation

#### Enhanced Reporting Features
- **One-Click Export**: Generate comprehensive system reports via "📊 Generate Report" button
- **Complete System Cards**: All 8 System Overview cards included in CSV format
- **Professional Organization**: Card-based CSV structure matching GUI layout
- **Comprehensive Data**: Hardware details, OS information, and complete software list
- **Timestamped Files**: Automatic filename generation with creation timestamp

#### Report Contents
1. **System Overview Section**:
   - All 8 system cards with detailed specifications
   - CPU, RAM, ROM, Battery, and Other Information cards
   - BIOS & Motherboard details with GPU detection

2. **Hardware Details Section**:
   - Complete CPU specifications (cores, frequencies, cache)
   - Memory information (total, available, usage percentages)
   - Storage details (partitions, drives, usage statistics)
   - GPU information with dedicated graphics detection
   - Network interfaces with IP addresses and statistics
   - Battery status and power information

3. **OS Details Section**:
   - Operating system configuration and version details
   - Network adapter specifications and IP configurations
   - **Complete Software List**: All installed software (not limited to top 10)

4. **System Tests Section**:
   - Latest test results and status information

### Running Tests

#### CPU Stress Test
- Duration: 10-300 seconds (configurable)
- Multi-core stress testing with real-time monitoring
- Temperature monitoring (if sensors available)
- Usage statistics and performance metrics

#### Memory Test
- Size: 10-1000 MB (configurable)
- Memory allocation and integrity testing
- Error detection and reporting

#### Disk Speed Test
- File size: 10-1000 MB (configurable)
- Sequential read/write speed benchmarking
- Temporary file creation and automatic cleanup

#### Network Speed Test
- Internet connectivity testing with speedtest-cli
- Download/upload speed measurement
- Ping latency testing and server information

### Auto-Refresh & User Experience
- Automatic data refresh every 30 seconds (toggleable)
- Manual refresh button for immediate updates
- Professional dark theme with glassmorphism design elements
- Non-blocking operations with threaded data collection
- Status bar updates and progress indicators

## Technical Details

### Architecture
- **Hardware Module**: Uses `psutil`, `py-cpuinfo`, `GPUtil`, and `wmi` for comprehensive hardware detection
- **OS Module**: Windows registry access and WMI queries for detailed OS information with complete software inventory
- **Testing Module**: Multi-threaded testing with callback-based progress reporting
- **GUI Module**: PySide6-based interface with worker threads for non-blocking operations
- **CSV Export**: Professional reporting system with card-based organization and complete data export

### Platform Support
- **Windows**: Full feature support with WMI integration and complete CSV reporting
- **Linux**: Basic hardware detection (WMI features and complete software listing unavailable)
- **macOS**: Limited testing, basic psutil functionality

### Performance Considerations
- Background data collection to prevent UI freezing
- Efficient memory usage with selective data loading
- Threaded test execution for responsive interface
- Optimized CSV generation with timeout protection for WMI queries

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
   - CSV reports will have limited software information

3. **Permission Errors**
   - Run as administrator for full hardware access
   - Some temperature sensors require elevated privileges
   - Complete software inventory requires registry access

4. **Network Test Failures**
   - Check internet connectivity
   - Firewall may block speedtest-cli

5. **CSV Generation Issues**
   - Ensure write permissions in application directory
   - WMI timeout protection prevents hanging on problematic queries
   - Large software lists may take extra time to process

### Error Messages
- Check the test_modules.py output for specific module errors
- GUI errors are displayed in the status bar
- Test failures show detailed error messages
- CSV generation errors display in popup dialogs

## Development

### File Structure
```
├── script.py              # Main application GUI
├── hardware_info.py       # Hardware detection module
├── os_info.py            # OS information module
├── system_tests.py       # Testing functionality
├── requirements.txt      # Python dependencies
├── test_modules.py       # Module testing script
├── README.md            # This file
└── system_report_*.csv   # Generated CSV reports (timestamped)
```

### Adding New Features
1. Hardware detection: Extend `HardwareInfo` class
2. OS information: Extend `OSInfo` class  
3. New tests: Add to `SystemTests` class
4. GUI components: Modify tabs in `script.py`
5. CSV reports: Update `generate_csv_report` method for new data sections

### Contributing
- Follow PEP 8 style guidelines
- Add error handling for new features
- Test on multiple platforms when possible
- Update requirements.txt for new dependencies
- Test CSV generation with various system configurations

## License

This project is open source and available under the MIT License.

## Version History

- **v1.2**: Enhanced CSV reporting with complete system cards and full software inventory
- **v1.1**: Fixed hardware details display and improved tree widget formatting
- **v1.0**: Initial release with full hardware/OS detection and testing capabilities

## Contact

For issues, suggestions, or contributions, please create an issue in the project repository.

---

**Note**: This application provides read-only system information and non-destructive testing. All tests are designed to be safe for normal computer operation. CSV reports contain comprehensive system information for documentation and analysis purposes.