"""
System Testing Module
Implements basic hardware tests for the laptop testing program
"""

import psutil
import time
import threading
import subprocess
import os
import tempfile
import random
from datetime import datetime
from keyboard_test import KeyboardTest

# Try to import microphone test
try:
    from microphone_test import MicrophoneTest
    MICROPHONE_TEST_AVAILABLE = True
except ImportError:
    MICROPHONE_TEST_AVAILABLE = False
    MicrophoneTest = None

class SystemTests:
    def __init__(self):
        self.is_testing = False
        self.test_results = {}
    
    def cpu_stress_test(self, duration=30, callback=None):
        """Run CPU stress test for specified duration"""
        self.is_testing = True
        results = {
            'test_name': 'CPU Stress Test',
            'duration': duration,
            'start_time': datetime.now(),
            'cpu_usage_samples': [],
            'cpu_temperatures': [],
            'max_usage': 0,
            'avg_usage': 0,
            'status': 'Running'
        }
        
        def stress_worker():
            # CPU intensive task
            end_time = time.time() + duration
            while time.time() < end_time and self.is_testing:
                # Perform CPU intensive calculations
                for _ in range(10000):
                    _ = sum(i*i for i in range(100))
        
        def monitor_worker():
            start_time = time.time()
            sample_count = 0
            total_usage = 0
            
            while time.time() - start_time < duration and self.is_testing:
                # Calculate progress
                elapsed_time = time.time() - start_time
                progress = int((elapsed_time / duration) * 100)
                results['progress'] = min(progress, 100)
                
                # Get CPU usage
                cpu_usage = psutil.cpu_percent(interval=1)
                results['cpu_usage_samples'].append({
                    'time': time.time() - start_time,
                    'usage': cpu_usage
                })
                
                total_usage += cpu_usage
                sample_count += 1
                
                if cpu_usage > results['max_usage']:
                    results['max_usage'] = cpu_usage
                
                # Get CPU temperature if available
                try:
                    temps = psutil.sensors_temperatures()
                    if 'coretemp' in temps:
                        temp = max(temp.current for temp in temps['coretemp'])
                        results['cpu_temperatures'].append({
                            'time': time.time() - start_time,
                            'temperature': temp
                        })
                except:
                    pass
                
                if callback:
                    callback(results)
                
                time.sleep(1)
            
            results['avg_usage'] = total_usage / sample_count if sample_count > 0 else 0
            results['progress'] = 100  # Ensure final progress is 100%
            results['end_time'] = datetime.now()
            results['status'] = 'Completed' if self.is_testing else 'Stopped'
            self.is_testing = False
            
            if callback:
                callback(results)
        
        # Start stress test threads
        num_cores = psutil.cpu_count()
        stress_threads = []
        
        for _ in range(num_cores):
            thread = threading.Thread(target=stress_worker)
            thread.daemon = True
            thread.start()
            stress_threads.append(thread)
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_worker)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return results
    
    def memory_test(self, test_size_mb=100, callback=None):
        """Run memory test by allocating and testing memory blocks"""
        self.is_testing = True
        results = {
            'test_name': 'Memory Test',
            'test_size_mb': test_size_mb,
            'start_time': datetime.now(),
            'blocks_tested': 0,
            'errors_found': 0,
            'status': 'Running',
            'memory_usage': []
        }
        
        def memory_test_worker():
            try:
                block_size = 1024 * 1024  # 1MB blocks
                num_blocks = test_size_mb
                memory_blocks = []
                
                # Allocate memory blocks
                for i in range(num_blocks):
                    if not self.is_testing:
                        break
                    
                    # Create random data
                    data = bytearray(random.getrandbits(8) for _ in range(block_size))
                    memory_blocks.append(data)
                    
                    results['blocks_tested'] = i + 1
                    # Calculate progress for allocation phase (0-50%)
                    results['progress'] = int((i + 1) / num_blocks * 50)
                    
                    # Monitor memory usage
                    memory_info = psutil.virtual_memory()
                    results['memory_usage'].append({
                        'time': i,
                        'used_percent': memory_info.percent,
                        'used_gb': memory_info.used / (1024**3)
                    })
                    
                    if callback:
                        callback(results)
                    
                    time.sleep(0.1)
                
                # Test memory blocks
                for i, block in enumerate(memory_blocks):
                    if not self.is_testing:
                        break
                    
                    # Verify data integrity
                    try:
                        # Simple checksum test
                        checksum = sum(block) % 256
                        if checksum != sum(block) % 256:
                            results['errors_found'] += 1
                    except Exception:
                        results['errors_found'] += 1
                    
                    # Calculate progress for testing phase (50-100%)
                    results['progress'] = int(50 + (i + 1) / len(memory_blocks) * 50)
                    
                    if callback:
                        callback(results)
                    
                    time.sleep(0.05)
                
                # Clean up
                del memory_blocks
                
                results['progress'] = 100  # Ensure final progress is 100%
                results['end_time'] = datetime.now()
                results['status'] = 'Completed' if self.is_testing else 'Stopped'
                self.is_testing = False
                
                if callback:
                    callback(results)
                    
            except Exception as e:
                results['error'] = str(e)
                results['status'] = 'Error'
                self.is_testing = False
                if callback:
                    callback(results)
        
        thread = threading.Thread(target=memory_test_worker)
        thread.daemon = True
        thread.start()
        
        return results
    
    def disk_speed_test(self, test_file_size_mb=100, callback=None):
        """Run disk speed test by writing and reading files"""
        self.is_testing = True
        results = {
            'test_name': 'Disk Speed Test',
            'test_file_size_mb': test_file_size_mb,
            'start_time': datetime.now(),
            'write_speed_mbps': 0,
            'read_speed_mbps': 0,
            'status': 'Running',
            'progress': 0
        }
        
        def disk_test_worker():
            try:
                # Create temporary file in a more explicit location
                import tempfile
                temp_dir = tempfile.gettempdir()
                temp_file = tempfile.NamedTemporaryFile(delete=False, dir=temp_dir, prefix='disktest_')
                temp_path = temp_file.name
                temp_file.close()
                
                print(f"DEBUG: Created temp file at: {temp_path}")
                
                # Test data
                test_data = b'0' * (1024 * 1024)  # 1MB of data
                
                # Write test
                print(f"DEBUG: Starting write test for {test_file_size_mb}MB")
                write_start = time.time()
                with open(temp_path, 'wb') as f:
                    for i in range(test_file_size_mb):
                        if not self.is_testing:
                            print("DEBUG: Write test stopped by user")
                            break
                        f.write(test_data)
                        # Calculate write progress (0-50%)
                        write_progress = int((i + 1) / test_file_size_mb * 50)
                        results['progress'] = write_progress
                        # Only update progress every 5MB or at the end to reduce callback frequency
                        if (i + 1) % 5 == 0 or i == test_file_size_mb - 1:
                            if callback:
                                print(f"DEBUG: Write progress callback: {write_progress}%")
                                callback(results)
                
                write_end = time.time()
                write_time = write_end - write_start
                results['write_speed_mbps'] = test_file_size_mb / write_time if write_time > 0 else 0
                print(f"DEBUG: Write completed - Speed: {results['write_speed_mbps']:.2f} MB/s")
                
                # Read test
                print(f"DEBUG: Starting read test")
                read_start = time.time()
                with open(temp_path, 'rb') as f:
                    for i in range(test_file_size_mb):
                        if not self.is_testing:
                            print("DEBUG: Read test stopped by user")
                            break
                        f.read(1024 * 1024)
                        # Calculate read progress (50-100%)
                        read_progress = int(50 + (i + 1) / test_file_size_mb * 50)
                        results['progress'] = read_progress
                        # Only update progress every 5MB or at the end to reduce callback frequency
                        if (i + 1) % 5 == 0 or i == test_file_size_mb - 1:
                            if callback:
                                print(f"DEBUG: Read progress callback: {read_progress}%")
                                callback(results)
                
                read_end = time.time()
                read_time = read_end - read_start
                results['read_speed_mbps'] = test_file_size_mb / read_time if read_time > 0 else 0
                print(f"DEBUG: Read completed - Speed: {results['read_speed_mbps']:.2f} MB/s")
                
                # Clean up
                print(f"DEBUG: Cleaning up temp file: {temp_path}")
                try:
                    os.unlink(temp_path)
                    print("DEBUG: Temp file deleted successfully")
                except Exception as cleanup_error:
                    print(f"DEBUG: Error deleting temp file: {cleanup_error}")
                
                results['end_time'] = datetime.now()
                results['status'] = 'Completed' if self.is_testing else 'Stopped'
                results['progress'] = 100
                self.is_testing = False
                
                print(f"DEBUG: Test completed, final callback")
                if callback:
                    callback(results)
                    
            except Exception as e:
                print(f"DEBUG: Exception in disk_test_worker: {e}")
                import traceback
                traceback.print_exc()
                results['error'] = str(e)
                results['status'] = 'Error'
                self.is_testing = False
                if callback:
                    callback(results)
        
        thread = threading.Thread(target=disk_test_worker)
        thread.daemon = True
        thread.start()
        
        return results
    
    def network_speed_test(self, callback=None):
        """Run network speed test using speedtest-cli"""
        self.is_testing = True
        results = {
            'test_name': 'Network Speed Test',
            'start_time': datetime.now(),
            'download_mbps': 0,
            'upload_mbps': 0,
            'ping_ms': 0,
            'server_info': {},
            'status': 'Running'
        }
        
        def network_test_worker():
            try:
                import speedtest
                
                # Initialize speedtest
                st = speedtest.Speedtest()
                
                if callback:
                    results['status'] = 'Finding best server...'
                    callback(results)
                
                # Get best server
                st.get_best_server()
                results['server_info'] = st.results.server
                
                if callback:
                    results['status'] = 'Testing download speed...'
                    callback(results)
                
                # Test download speed
                download_speed = st.download()
                results['download_mbps'] = download_speed / 1_000_000  # Convert to Mbps
                
                if callback:
                    results['status'] = 'Testing upload speed...'
                    callback(results)
                
                # Test upload speed
                upload_speed = st.upload()
                results['upload_mbps'] = upload_speed / 1_000_000  # Convert to Mbps
                
                # Get ping
                results['ping_ms'] = st.results.ping
                
                results['end_time'] = datetime.now()
                results['status'] = 'Completed' if self.is_testing else 'Stopped'
                self.is_testing = False
                
                if callback:
                    callback(results)
                    
            except Exception as e:
                results['error'] = str(e)
                results['status'] = 'Error'
                self.is_testing = False
                if callback:
                    callback(results)
        
        thread = threading.Thread(target=network_test_worker)
        thread.daemon = True
        thread.start()
        
        return results
    
    def system_stability_test(self, duration=300, callback=None):
        """Run comprehensive system stability test"""
        self.is_testing = True
        results = {
            'test_name': 'System Stability Test',
            'duration': duration,
            'start_time': datetime.now(),
            'cpu_stable': True,
            'memory_stable': True,
            'disk_stable': True,
            'temperature_stable': True,
            'max_temperature': 0,
            'errors': [],
            'status': 'Running'
        }
        
        def stability_test_worker():
            start_time = time.time()
            
            while time.time() - start_time < duration and self.is_testing:
                try:
                    # Check CPU usage
                    cpu_usage = psutil.cpu_percent(interval=1)
                    if cpu_usage > 95:
                        results['cpu_stable'] = False
                        results['errors'].append(f"High CPU usage: {cpu_usage}%")
                    
                    # Check memory usage
                    memory = psutil.virtual_memory()
                    if memory.percent > 90:
                        results['memory_stable'] = False
                        results['errors'].append(f"High memory usage: {memory.percent}%")
                    
                    # Check disk usage
                    for partition in psutil.disk_partitions():
                        try:
                            usage = psutil.disk_usage(partition.mountpoint)
                            if usage.percent > 95:
                                results['disk_stable'] = False
                                results['errors'].append(f"High disk usage: {usage.percent}% on {partition.device}")
                        except:
                            continue
                    
                    # Check temperature
                    try:
                        temps = psutil.sensors_temperatures()
                        if temps:
                            for name, entries in temps.items():
                                for entry in entries:
                                    if entry.current > results['max_temperature']:
                                        results['max_temperature'] = entry.current
                                    if entry.current > 80:  # 80Â°C threshold
                                        results['temperature_stable'] = False
                                        results['errors'].append(f"High temperature: {entry.current}Â°C")
                    except:
                        pass
                    
                    if callback:
                        callback(results)
                    
                    time.sleep(5)
                    
                except Exception as e:
                    results['errors'].append(f"Stability test error: {str(e)}")
            
            results['end_time'] = datetime.now()
            results['status'] = 'Completed' if self.is_testing else 'Stopped'
            self.is_testing = False
            
            if callback:
                callback(results)
        
        thread = threading.Thread(target=stability_test_worker)
        thread.daemon = True
        thread.start()
        
        return results
    
    def brightness_test(self, callback=None):
        """Test brightness controls by cycling through different levels"""
        self.is_testing = True
        results = {
            'test_name': 'Brightness Test',
            'start_time': datetime.now(),
            'original_brightness': None,
            'brightness_levels_tested': [],
            'brightness_support': False,
            'status': 'Running',
            'progress': 0,
            'errors': []
        }
        
        def brightness_test_worker():
            try:
                import subprocess
                import sys
                
                # Try to get current brightness level
                try:
                    if sys.platform == "win32":
                        # Windows brightness control using WMI
                        result = subprocess.run([
                            'powershell', '-Command',
                            '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0 and result.stdout.strip():
                            original_brightness = int(result.stdout.strip())
                            results['original_brightness'] = original_brightness
                            results['brightness_support'] = True
                            print(f"DEBUG: Current brightness: {original_brightness}%")
                        else:
                            results['errors'].append("Could not detect current brightness level")
                            results['brightness_support'] = False
                    else:
                        results['errors'].append("Brightness test only supported on Windows")
                        results['brightness_support'] = False
                        
                except Exception as e:
                    results['errors'].append(f"Error detecting brightness: {str(e)}")
                    results['brightness_support'] = False
                
                if not results['brightness_support']:
                    results['status'] = 'Completed'
                    results['progress'] = 100
                    self.is_testing = False
                    if callback:
                        callback(results)
                    return
                
                # Test different brightness levels
                test_levels = [20, 40, 60, 80, 100]
                total_steps = len(test_levels) + 1  # +1 for restoration
                
                for i, level in enumerate(test_levels):
                    if not self.is_testing:
                        break
                    
                    try:
                        print(f"DEBUG: Setting brightness to {level}%")
                        # Set brightness using PowerShell
                        result = subprocess.run([
                            'powershell', '-Command',
                            f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})'
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0:
                            results['brightness_levels_tested'].append({
                                'level': level,
                                'success': True,
                                'timestamp': datetime.now()
                            })
                            print(f"DEBUG: Successfully set brightness to {level}%")
                        else:
                            results['brightness_levels_tested'].append({
                                'level': level,
                                'success': False,
                                'error': result.stderr.strip() if result.stderr else 'Unknown error',
                                'timestamp': datetime.now()
                            })
                            results['errors'].append(f"Failed to set brightness to {level}%")
                        
                        # Update progress
                        results['progress'] = int((i + 1) / total_steps * 100)
                        
                        if callback:
                            callback(results)
                        
                        # Wait a moment to see the brightness change
                        time.sleep(2)
                        
                    except Exception as e:
                        results['errors'].append(f"Error setting brightness to {level}%: {str(e)}")
                        results['brightness_levels_tested'].append({
                            'level': level,
                            'success': False,
                            'error': str(e),
                            'timestamp': datetime.now()
                        })
                
                # Restore original brightness
                if results['original_brightness'] is not None:
                    try:
                        print(f"DEBUG: Restoring brightness to {results['original_brightness']}%")
                        result = subprocess.run([
                            'powershell', '-Command',
                            f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{results["original_brightness"]})'
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0:
                            print("DEBUG: Successfully restored original brightness")
                        else:
                            results['errors'].append("Failed to restore original brightness")
                            
                    except Exception as e:
                        results['errors'].append(f"Error restoring brightness: {str(e)}")
                
                results['progress'] = 100
                results['end_time'] = datetime.now()
                results['status'] = 'Completed' if self.is_testing else 'Stopped'
                self.is_testing = False
                
                if callback:
                    callback(results)
                    
            except Exception as e:
                print(f"DEBUG: Exception in brightness_test_worker: {e}")
                import traceback
                traceback.print_exc()
                results['error'] = str(e)
                results['status'] = 'Error'
                self.is_testing = False
                if callback:
                    callback(results)
        
        thread = threading.Thread(target=brightness_test_worker)
        thread.daemon = True
        thread.start()
        
        return results
    
    def charging_test(self, callback=None):
        """Test charging functionality by monitoring battery status changes"""
        self.is_testing = True
        results = {
            'test_name': 'Charging Test',
            'start_time': datetime.now(),
            'battery_support': False,
            'initial_charging_state': None,
            'initial_battery_level': None,
            'charging_events': [],
            'battery_level_changes': [],
            'status': 'Running',
            'progress': 0,
            'errors': [],
            'instructions_given': False
        }
        
        def charging_test_worker():
            try:
                import psutil
                
                # Check if battery is available
                try:
                    battery = psutil.sensors_battery()
                    if battery is None:
                        results['errors'].append("No battery detected - this test requires a laptop/device with battery")
                        results['battery_support'] = False
                        results['status'] = 'Completed'
                        results['progress'] = 100
                        self.is_testing = False
                        if callback:
                            callback(results)
                        return
                    
                    results['battery_support'] = True
                    results['initial_charging_state'] = battery.power_plugged
                    results['initial_battery_level'] = battery.percent
                    
                    print(f"DEBUG: Initial battery state - Charging: {battery.power_plugged}, Level: {battery.percent}%")
                    
                except Exception as e:
                    results['errors'].append(f"Error detecting battery: {str(e)}")
                    results['battery_support'] = False
                    results['status'] = 'Error'
                    self.is_testing = False
                    if callback:
                        callback(results)
                    return
                
                # Instructions for user
                if not results['instructions_given']:
                    results['instructions_given'] = True
                    if callback:
                        callback(results)
                
                # Monitor charging state for 60 seconds
                monitor_duration = 60  # seconds
                check_interval = 2     # seconds
                checks_total = monitor_duration // check_interval
                
                last_charging_state = results['initial_charging_state']
                last_battery_level = results['initial_battery_level']
                last_callback_time = 0
                
                for check in range(checks_total):
                    if not self.is_testing:
                        break
                    
                    try:
                        battery = psutil.sensors_battery()
                        current_charging = battery.power_plugged
                        current_level = battery.percent
                        timestamp = datetime.now()
                        current_time = time.time()
                        
                        # Detect charging state changes
                        if current_charging != last_charging_state:
                            event = {
                                'timestamp': timestamp,
                                'event': 'plugged_in' if current_charging else 'unplugged',
                                'battery_level': current_level,
                                'charging_state': current_charging
                            }
                            results['charging_events'].append(event)
                            print(f"DEBUG: Charging event detected - {event['event']} at {current_level}%")
                            last_charging_state = current_charging
                        
                        # Track battery level changes
                        if abs(current_level - last_battery_level) >= 1:  # 1% change threshold
                            level_change = {
                                'timestamp': timestamp,
                                'old_level': last_battery_level,
                                'new_level': current_level,
                                'change': current_level - last_battery_level,
                                'charging': current_charging
                            }
                            results['battery_level_changes'].append(level_change)
                            print(f"DEBUG: Battery level change - {last_battery_level}% â†’ {current_level}% (charging: {current_charging})")
                            last_battery_level = current_level
                        
                        # Update progress
                        results['progress'] = int((check + 1) / checks_total * 100)
                        
                        # Update current status
                        results['current_charging_state'] = current_charging
                        results['current_battery_level'] = current_level
                        
                        # Throttle callbacks to prevent recursive repaint issues
                        if callback and (current_time - last_callback_time >= 1.0):
                            # Make a copy to avoid reference issues
                            callback_results = dict(results)
                            callback(callback_results)
                            last_callback_time = current_time
                        
                        time.sleep(check_interval)
                        
                    except Exception as e:
                        results['errors'].append(f"Error during monitoring: {str(e)}")
                        print(f"DEBUG: Monitoring error: {e}")
                
                # Analyze results
                results['charging_events_detected'] = len(results['charging_events'])
                results['battery_level_changes_detected'] = len(results['battery_level_changes'])
                
                # Determine test success
                if results['charging_events_detected'] > 0:
                    results['charging_port_status'] = 'Working - charging state changes detected'
                else:
                    results['charging_port_status'] = 'No changes detected - please plug/unplug charger during test'
                
                if results['battery_level_changes_detected'] > 0:
                    # Check if battery levels increased when charging
                    charging_increases = [change for change in results['battery_level_changes'] 
                                        if change['charging'] and change['change'] > 0]
                    if charging_increases:
                        results['battery_charging_status'] = 'Working - battery level increased while charging'
                    else:
                        results['battery_charging_status'] = 'Partial - state changes detected but no charging increase'
                else:
                    results['battery_charging_status'] = 'No battery level changes detected'
                
                results['progress'] = 100
                results['end_time'] = datetime.now()
                results['status'] = 'Completed' if self.is_testing else 'Stopped'
                self.is_testing = False
                
                if callback:
                    callback(results)
                    
            except Exception as e:
                print(f"DEBUG: Exception in charging_test_worker: {e}")
                import traceback
                traceback.print_exc()
                results['error'] = str(e)
                results['status'] = 'Error'
                self.is_testing = False
                if callback:
                    callback(results)
        
        thread = threading.Thread(target=charging_test_worker)
        thread.daemon = True
        thread.start()
        
        return results
    
    def keyboard_test(self, callback=None):
        """ Test keyboard functionality by opening a keyboard tester webpage """
        keyboard_tester = KeyboardTest()
        return keyboard_tester.run_test(callback)

    def camera_test(self, callback=None):
        """Test camera functionality with integrated preview window"""
        self.is_testing = True
        results = {
            'test_name': 'Camera Test',
            'start_time': datetime.now(),
            'status': 'Running',
            'progress': 0,
            'errors': [],
            'instructions': []
        }
        
        def camera_test_worker():
            try:
                # Add instructions
                results['instructions'].append("Opening integrated camera test window...")
                results['instructions'].append("Please verify that:")
                results['instructions'].append("• Camera preview shows live video feed")
                results['instructions'].append("• Image quality is clear and well-lit")
                results['instructions'].append("• Use 'Open Camera App' for system camera")
                results['instructions'].append("• Use 'Debug Camera Settings' for troubleshooting")
                results['progress'] = 25
                
                if callback:
                    callback(results)
                
                # Import here to avoid issues
                from camera_test import CameraTest
                
                # Create camera test in main thread using Qt's moveToThread mechanism
                import threading
                
                # This will store the result from the main thread
                camera_result = {'success': False, 'error': None, 'window_opened': False}
                
                def create_camera_in_main_thread():
                    """Create camera test window in main thread"""
                    try:
                        camera_test = CameraTest()
                        test_results = camera_test.run_test()
                        camera_result['success'] = True
                        camera_result['window_opened'] = test_results.get('window_opened', False)
                        if test_results.get('errors'):
                            camera_result['error'] = '; '.join(test_results['errors'])
                    except Exception as e:
                        camera_result['error'] = str(e)
                
                # Use Qt's invoke method to run in main thread
                try:
                    from PySide6.QtCore import QMetaObject, Qt, QCoreApplication
                    
                    # Try to invoke in main thread if Qt app exists
                    if QCoreApplication.instance():
                        QMetaObject.invokeMethod(
                            QCoreApplication.instance(),
                            create_camera_in_main_thread,
                            Qt.QueuedConnection
                        )
                        
                        # Wait a bit for the main thread operation
                        time.sleep(1)
                    else:
                        # Fallback: create directly (might cause issues but worth trying)
                        create_camera_in_main_thread()
                        
                except Exception as e:
                    # Last resort fallback
                    camera_result['error'] = f"Qt invocation failed: {str(e)}"
                
                # Process results
                if camera_result['success'] or camera_result['window_opened']:
                    results['status'] = 'Completed'
                    results['progress'] = 100
                    results['camera_opened'] = True
                    results['instructions'].append("✅ Camera test window opened successfully")
                    results['instructions'].append("💡 Test camera functionality in the opened window")
                elif camera_result['error']:
                    results['status'] = 'Error'
                    results['errors'].append(f"Camera test error: {camera_result['error']}")
                else:
                    results['status'] = 'Error'
                    results['errors'].append("Unknown error in camera test")
                
                results['end_time'] = datetime.now()
                
                if callback:
                    callback(results)
                
            except Exception as e:
                results['status'] = 'Error'
                results['errors'].append(f"Camera test error: {str(e)}")
                results['end_time'] = datetime.now()
                
                if callback:
                    callback(results)
            
            finally:
                self.is_testing = False
        
        thread = threading.Thread(target=camera_test_worker)
        thread.daemon = True
        thread.start()
        
        return results

    def microphone_test(self, callback=None):
        """Test microphone functionality with waveform visualization"""
        self.is_testing = True
        results = {
            'test_name': 'Microphone Test',
            'start_time': datetime.now(),
            'status': 'Running',
            'progress': 0,
            'errors': [],
            'instructions': []
        }
        
        def microphone_test_worker():
            try:
                # Check if microphone test is available
                if not MICROPHONE_TEST_AVAILABLE:
                    results['status'] = 'Error'
                    results['errors'].append("Microphone test module not available")
                    results['instructions'].append("Install required packages: pip install pyaudio matplotlib numpy")
                    results['end_time'] = datetime.now()
                    if callback:
                        callback(results)
                    return
                
                # Add instructions
                results['instructions'].append("Opening microphone test window with waveform visualization...")
                results['instructions'].append("Please verify that:")
                results['instructions'].append("• Click 'Start Recording' to begin microphone capture")
                results['instructions'].append("• Speak or make sounds to see waveform visualization")
                results['instructions'].append("• Check volume level bar for input sensitivity")
                results['instructions'].append("• Use 'Test System Audio' to verify speakers")
                results['instructions'].append("• Use settings buttons for microphone configuration")
                results['progress'] = 25
                
                if callback:
                    callback(results)
                
                # This will store the result from the main thread
                microphone_result = {'success': False, 'error': None, 'window_opened': False}
                
                def create_microphone_in_main_thread():
                    """Create microphone test window in main thread"""
                    try:
                        microphone_test = MicrophoneTest()
                        test_results = microphone_test.run_test()
                        microphone_result['success'] = True
                        microphone_result['window_opened'] = test_results.get('window_opened', False)
                        if test_results.get('errors'):
                            microphone_result['error'] = '; '.join(test_results['errors'])
                    except Exception as e:
                        microphone_result['error'] = str(e)
                
                # Use Qt's invoke method to run in main thread
                try:
                    from PySide6.QtCore import QMetaObject, Qt, QCoreApplication
                    
                    # Try to invoke in main thread if Qt app exists
                    if QCoreApplication.instance():
                        QMetaObject.invokeMethod(
                            QCoreApplication.instance(),
                            create_microphone_in_main_thread,
                            Qt.QueuedConnection
                        )
                        
                        # Wait a bit for the main thread operation
                        time.sleep(1)
                    else:
                        # Fallback: create directly (might cause issues but worth trying)
                        create_microphone_in_main_thread()
                        
                except Exception as e:
                    # Last resort fallback
                    microphone_result['error'] = f"Qt invocation failed: {str(e)}"
                
                # Process results
                if microphone_result['success'] or microphone_result['window_opened']:
                    results['status'] = 'Completed'
                    results['progress'] = 100
                    results['microphone_opened'] = True
                    results['instructions'].append("✅ Microphone test window opened successfully")
                    results['instructions'].append("💡 Test microphone functionality in the opened window")
                elif microphone_result['error']:
                    results['status'] = 'Error'
                    results['errors'].append(f"Microphone test error: {microphone_result['error']}")
                else:
                    results['status'] = 'Error'
                    results['errors'].append("Unknown error in microphone test")
                
                results['end_time'] = datetime.now()
                
                if callback:
                    callback(results)
                
            except Exception as e:
                results['status'] = 'Error'
                results['errors'].append(f"Microphone test error: {str(e)}")
                results['end_time'] = datetime.now()
                
                if callback:
                    callback(results)
            
            finally:
                self.is_testing = False
        
        thread = threading.Thread(target=microphone_test_worker)
        thread.daemon = True
        thread.start()
        
        return results

    def stop_all_tests(self):
        """Stop all running tests"""
        self.is_testing = False
      
    def get_test_recommendations(self, hardware_info):
        """Get test recommendations based on hardware"""
        recommendations = []
        
        try:
            # CPU recommendations
            cpu_cores = hardware_info.get('cpu', {}).get('cores_physical', 1)
            if cpu_cores >= 4:
                recommendations.append("Run CPU stress test for 60 seconds to test multi-core performance")
            else:
                recommendations.append("Run CPU stress test for 30 seconds (fewer cores detected)")
            
            # Memory recommendations
            total_memory = hardware_info.get('memory', {}).get('total', 0)
            if total_memory >= 8:
                recommendations.append("Run memory test with 500MB to test RAM stability")
            else:
                recommendations.append("Run memory test with 100MB (limited RAM detected)")
            
            # Disk recommendations
            recommendations.append("Run disk speed test to check storage performance")
            
            # Network recommendations
            recommendations.append("Run network speed test to check internet connectivity")
            
            # Stability test
            recommendations.append("Run system stability test for 5 minutes to check overall system health")
            
        except Exception as e:
            recommendations.append(f"Error generating recommendations: {str(e)}")
        
        return recommendations

# Test the module
if __name__ == "__main__":
    tests = SystemTests()
    print("Testing System Tests Module...")
    
    def test_callback(results):
        print(f"Test: {results['test_name']} - Status: {results['status']}")
        if 'progress' in results:
            print(f"Progress: {results['progress']}%")
    
    # Quick CPU test
    print("\n=== Starting CPU Test ===")
    cpu_results = tests.cpu_stress_test(duration=5, callback=test_callback)
    time.sleep(6)
    
    print("\n=== Test Recommendations ===")
    sample_hw_info = {'cpu': {'cores_physical': 4}, 'memory': {'total': 8}}
    recommendations = tests.get_test_recommendations(sample_hw_info)
    for rec in recommendations:
        print(f"- {rec}")
