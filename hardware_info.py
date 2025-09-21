"""
Hardware Information Module
Collects detailed hardware information about the laptop/computer
"""

import psutil
import platform
import socket
import uuid
import cpuinfo
import GPUtil
import sys
from datetime import datetime
import subprocess
import os

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

class HardwareInfo:
    def __init__(self):
        self.cpu_info = None
        self.memory_info = None
        self.disk_info = None
        self.gpu_info = None
        self.network_info = None
        self.system_info = None
        
        if WMI_AVAILABLE:
            try:
                self.wmi = wmi.WMI()
            except:
                self.wmi = None
        else:
            self.wmi = None
    
    def get_cpu_info(self):
        """Get detailed CPU information"""
        try:
            cpu_data = cpuinfo.get_cpu_info()
            
            info = {
                'name': cpu_data.get('brand_raw', 'Unknown'),
                'architecture': cpu_data.get('arch', platform.machine()),
                'cores_physical': psutil.cpu_count(logical=False),
                'cores_logical': psutil.cpu_count(logical=True),
                'frequency_current': psutil.cpu_freq().current if psutil.cpu_freq() else 'Unknown',
                'frequency_max': psutil.cpu_freq().max if psutil.cpu_freq() else 'Unknown',
                'frequency_min': psutil.cpu_freq().min if psutil.cpu_freq() else 'Unknown',
                'usage_percent': psutil.cpu_percent(interval=1),
                'cache_l1': cpu_data.get('l1_cache_size', 'Unknown'),
                'cache_l2': cpu_data.get('l2_cache_size', 'Unknown'),
                'cache_l3': cpu_data.get('l3_cache_size', 'Unknown'),
                'vendor': cpu_data.get('vendor_id_raw', 'Unknown'),
                'family': cpu_data.get('family', 'Unknown'),
                'model': cpu_data.get('model', 'Unknown'),
                'stepping': cpu_data.get('stepping', 'Unknown'),
                'flags': cpu_data.get('flags', []),
            }
            
            # Get per-core usage
            info['usage_per_core'] = psutil.cpu_percent(percpu=True, interval=1)
            
            # Get CPU temperatures if available
            try:
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps:
                    info['temperature'] = [temp.current for temp in temps['coretemp']]
                elif 'cpu_thermal' in temps:
                    info['temperature'] = [temp.current for temp in temps['cpu_thermal']]
                else:
                    info['temperature'] = 'Not available'
            except:
                info['temperature'] = 'Not available'
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def get_memory_info(self):
        """Get detailed memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            info = {
                'total': self._bytes_to_gb(memory.total),
                'available': self._bytes_to_gb(memory.available),
                'used': self._bytes_to_gb(memory.used),
                'percentage': memory.percent,
                'swap_total': self._bytes_to_gb(swap.total),
                'swap_used': self._bytes_to_gb(swap.used),
                'swap_free': self._bytes_to_gb(swap.free),
                'swap_percentage': swap.percent,
            }
            
            # Get memory slots information if WMI is available
            if self.wmi:
                try:
                    # Try to initialize COM for this thread
                    import pythoncom
                    pythoncom.CoInitialize()
                    
                    memory_slots = []
                    for memory_module in self.wmi.Win32_PhysicalMemory():
                        slot_info = {
                            'capacity': self._bytes_to_gb(int(memory_module.Capacity)),
                            'speed': memory_module.Speed,
                            'manufacturer': memory_module.Manufacturer,
                            'serial_number': memory_module.SerialNumber,
                            'part_number': memory_module.PartNumber,
                            'memory_type': memory_module.MemoryType,
                            'form_factor': memory_module.FormFactor,
                            'device_locator': memory_module.DeviceLocator,
                        }
                        memory_slots.append(slot_info)
                    info['memory_slots'] = memory_slots
                except:
                    # Fallback: Try direct WMI connection
                    try:
                        import wmi
                        import pythoncom
                        pythoncom.CoInitialize()
                        local_wmi = wmi.WMI()
                        
                        memory_slots = []
                        for memory_module in local_wmi.Win32_PhysicalMemory():
                            slot_info = {
                                'capacity': self._bytes_to_gb(int(memory_module.Capacity)),
                                'speed': memory_module.Speed,
                                'manufacturer': memory_module.Manufacturer,
                                'serial_number': memory_module.SerialNumber,
                                'part_number': memory_module.PartNumber,
                                'memory_type': memory_module.MemoryType,
                                'form_factor': memory_module.FormFactor,
                                'device_locator': memory_module.DeviceLocator,
                            }
                            memory_slots.append(slot_info)
                        info['memory_slots'] = memory_slots
                    except:
                        info['memory_slots'] = 'Not available'
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def get_disk_info(self):
        """Get detailed disk information"""
        try:
            # Initialize COM for this thread
            try:
                import pythoncom
                pythoncom.CoInitialize()
            except:
                pass  # COM might already be initialized or not available
                
            disks = []
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info = {
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total': self._bytes_to_gb(usage.total),
                        'used': self._bytes_to_gb(usage.used),
                        'free': self._bytes_to_gb(usage.free),
                        'percentage': (usage.used / usage.total) * 100 if usage.total > 0 else 0,
                    }
                    disks.append(disk_info)
                except PermissionError:
                    continue
            
            # Get disk I/O statistics
            try:
                disk_io = psutil.disk_io_counters()
                io_info = {
                    'read_count': disk_io.read_count,
                    'write_count': disk_io.write_count,
                    'read_bytes': self._bytes_to_gb(disk_io.read_bytes),
                    'write_bytes': self._bytes_to_gb(disk_io.write_bytes),
                    'read_time': disk_io.read_time,
                    'write_time': disk_io.write_time,
                }
            except:
                io_info = 'Not available'
            
            # Get physical disk information if WMI is available
            physical_disks = []
            try:
                # For threaded contexts, create a fresh WMI connection
                import wmi
                thread_wmi = wmi.WMI()
                
                for disk in thread_wmi.Win32_DiskDrive():
                    disk_info = {
                        'model': disk.Model,
                        'serial_number': disk.SerialNumber,
                        'size': self._bytes_to_gb(int(disk.Size)) if disk.Size else 'Unknown',
                        'interface_type': disk.InterfaceType,
                        'media_type': disk.MediaType,
                        'status': disk.Status,
                    }
                    physical_disks.append(disk_info)
            except Exception as e:
                # Fallback to the original WMI connection if available
                if self.wmi:
                    try:
                        for disk in self.wmi.Win32_DiskDrive():
                            disk_info = {
                                'model': disk.Model,
                                'serial_number': disk.SerialNumber,
                                'size': self._bytes_to_gb(int(disk.Size)) if disk.Size else 'Unknown',
                                'interface_type': disk.InterfaceType,
                                'media_type': disk.MediaType,
                                'status': disk.Status,
                            }
                            physical_disks.append(disk_info)
                    except:
                        pass
            
            return {
                'partitions': disks,
                'io_statistics': io_info,
                'physical_disks': physical_disks,
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_gpu_info(self):
        """Get detailed GPU information"""
        try:
            gpus = []
            
            # Get NVIDIA GPUs using GPUtil
            try:
                nvidia_gpus = GPUtil.getGPUs()
                for gpu in nvidia_gpus:
                    gpu_info = {
                        'name': gpu.name,
                        'id': gpu.id,
                        'memory_total': gpu.memoryTotal,
                        'memory_used': gpu.memoryUsed,
                        'memory_free': gpu.memoryFree,
                        'memory_percentage': (gpu.memoryUsed / gpu.memoryTotal) * 100,
                        'temperature': gpu.temperature,
                        'load': gpu.load * 100,
                        'driver': gpu.driver,
                        'vendor': 'NVIDIA',
                    }
                    gpus.append(gpu_info)
            except:
                pass
            
            # Get all GPU information using WMI if available
            if self.wmi:
                try:
                    for gpu in self.wmi.Win32_VideoController():
                        if gpu.Name and 'microsoft' not in gpu.Name.lower():
                            gpu_info = {
                                'name': gpu.Name,
                                'driver_version': gpu.DriverVersion,
                                'driver_date': gpu.DriverDate,
                                'adapter_ram': self._bytes_to_gb(int(gpu.AdapterRAM)) if gpu.AdapterRAM else 'Unknown',
                                'video_processor': gpu.VideoProcessor,
                                'status': gpu.Status,
                                'pnp_device_id': gpu.PNPDeviceID,
                                'vendor': 'Other',
                            }
                            # Check if this GPU is already in the list (to avoid duplicates)
                            if not any(g['name'] == gpu_info['name'] for g in gpus):
                                gpus.append(gpu_info)
                except:
                    pass
            
            return gpus if gpus else [{'name': 'No dedicated GPU found', 'vendor': 'Integrated'}]
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_network_info(self):
        """Get detailed network information"""
        try:
            network_info = {}
            
            # Get network interfaces
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            io_counters = psutil.net_io_counters(pernic=True)
            
            network_interfaces = []
            for interface_name, addresses in interfaces.items():
                interface_info = {
                    'name': interface_name,
                    'addresses': [],
                    'is_up': stats[interface_name].isup if interface_name in stats else False,
                    'speed': stats[interface_name].speed if interface_name in stats else 'Unknown',
                    'mtu': stats[interface_name].mtu if interface_name in stats else 'Unknown',
                }
                
                for address in addresses:
                    addr_info = {
                        'family': str(address.family),
                        'address': address.address,
                        'netmask': address.netmask,
                        'broadcast': address.broadcast,
                    }
                    interface_info['addresses'].append(addr_info)
                
                if interface_name in io_counters:
                    interface_info['io'] = {
                        'bytes_sent': self._bytes_to_mb(io_counters[interface_name].bytes_sent),
                        'bytes_recv': self._bytes_to_mb(io_counters[interface_name].bytes_recv),
                        'packets_sent': io_counters[interface_name].packets_sent,
                        'packets_recv': io_counters[interface_name].packets_recv,
                    }
                
                network_interfaces.append(interface_info)
            
            network_info['interfaces'] = network_interfaces
            
            # Get default gateway and hostname
            try:
                network_info['hostname'] = socket.gethostname()
                network_info['fqdn'] = socket.getfqdn()
            except:
                network_info['hostname'] = 'Unknown'
                network_info['fqdn'] = 'Unknown'
            
            return network_info
        except Exception as e:
            return {'error': str(e)}
    
    def get_system_info(self):
        """Get detailed system information"""
        try:
            info = {
                'hostname': platform.node(),
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'architecture': platform.architecture(),
                'python_version': platform.python_version(),
                'python_implementation': platform.python_implementation(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
                'uptime': str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())),
            }
            
            # Get MAC address
            try:
                info['mac_address'] = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                                              for ele in range(0,8*6,8)][::-1])
            except:
                info['mac_address'] = 'Unknown'
            
            # Get BIOS information if WMI is available
            if self.wmi:
                try:
                    # Try to initialize COM for this thread
                    import pythoncom
                    pythoncom.CoInitialize()
                    
                    for bios in self.wmi.Win32_BIOS():
                        info['bios_version'] = bios.Version
                        info['bios_manufacturer'] = bios.Manufacturer
                        info['bios_serial'] = bios.SerialNumber
                        info['bios_date'] = bios.ReleaseDate
                        break
                except Exception as e:
                    pass
                
                # Get motherboard information
                try:
                    for board in self.wmi.Win32_BaseBoard():
                        info['motherboard_manufacturer'] = board.Manufacturer
                        info['motherboard_product'] = board.Product
                        info['motherboard_serial'] = board.SerialNumber
                        break
                except Exception as e:
                    pass
                
                # Get system information
                try:
                    for system in self.wmi.Win32_ComputerSystem():
                        info['computer_manufacturer'] = system.Manufacturer
                        info['computer_model'] = system.Model
                        info['total_physical_memory'] = self._bytes_to_gb(int(system.TotalPhysicalMemory))
                        break
                except Exception as e:
                    pass
            
            # Fallback: Try direct WMI connection if the above failed
            if 'computer_manufacturer' not in info or info.get('computer_manufacturer') is None:
                try:
                    import wmi
                    import pythoncom
                    pythoncom.CoInitialize()
                    local_wmi = wmi.WMI()
                    
                    for system in local_wmi.Win32_ComputerSystem():
                        info['computer_manufacturer'] = system.Manufacturer
                        info['computer_model'] = system.Model
                        break
                        
                    for bios in local_wmi.Win32_BIOS():
                        info['bios_version'] = bios.Version
                        info['bios_manufacturer'] = bios.Manufacturer
                        info['bios_serial'] = bios.SerialNumber
                        info['bios_date'] = bios.ReleaseDate
                        break
                        
                    for board in local_wmi.Win32_BaseBoard():
                        info['motherboard_manufacturer'] = board.Manufacturer
                        info['motherboard_product'] = board.Product
                        info['motherboard_serial'] = board.SerialNumber
                        break
                        
                except Exception as e:
                    pass
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def get_battery_info(self):
        """Get battery information"""
        try:
            # Get basic battery info from psutil
            battery = psutil.sensors_battery()
            battery_info = {}
            
            if battery:
                battery_info.update({
                    'percent': battery.percent,
                    'power_plugged': battery.power_plugged,
                    'time_left': str(battery.secsleft) + ' seconds' if battery.secsleft != psutil.POWER_TIME_UNLIMITED else 'Unlimited'
                })
            
            # Get detailed battery info from WMI
            try:
                import pythoncom
                pythoncom.CoInitialize()
                c = wmi.WMI()
                
                # Query battery static data
                for battery_static in c.Win32_Battery():
                    if hasattr(battery_static, 'Name') and battery_static.Name:
                        battery_info['name'] = battery_static.Name
                    if hasattr(battery_static, 'DesignCapacity') and battery_static.DesignCapacity:
                        battery_info['design_capacity'] = battery_static.DesignCapacity
                    if hasattr(battery_static, 'FullChargeCapacity') and battery_static.FullChargeCapacity:
                        battery_info['full_charge_capacity'] = battery_static.FullChargeCapacity
                    if hasattr(battery_static, 'Chemistry') and battery_static.Chemistry:
                        chemistry_map = {
                            1: 'Other', 2: 'Unknown', 3: 'Lead Acid', 4: 'Nickel Cadmium',
                            5: 'Nickel Metal Hydride', 6: 'Lithium Ion', 7: 'Zinc Air',
                            8: 'Lithium Polymer'
                        }
                        battery_info['chemistry'] = chemistry_map.get(battery_static.Chemistry, f'Unknown ({battery_static.Chemistry})')
                    if hasattr(battery_static, 'DesignVoltage') and battery_static.DesignVoltage:
                        battery_info['design_voltage'] = battery_static.DesignVoltage
                    if hasattr(battery_static, 'EstimatedChargeRemaining') and battery_static.EstimatedChargeRemaining is not None:
                        battery_info['charge_remaining'] = battery_static.EstimatedChargeRemaining
                    if hasattr(battery_static, 'BatteryStatus') and battery_static.BatteryStatus:
                        status_map = {
                            1: 'Discharging', 2: 'Charging', 3: 'Critical', 4: 'Low',
                            5: 'High', 6: 'Recharging', 7: 'Charging/High', 8: 'Charging/Low',
                            9: 'Charging/Critical', 10: 'Undefined', 11: 'Partially Charged'
                        }
                        battery_info['detailed_status'] = status_map.get(battery_static.BatteryStatus, f'Unknown ({battery_static.BatteryStatus})')
                
                # Try to get cycle count from different WMI classes
                cycle_count_found = False
                
                # Method 1: CIM_Battery
                for cim_battery in c.CIM_Battery():
                    if hasattr(cim_battery, 'CycleCount') and cim_battery.CycleCount is not None:
                        battery_info['cycle_count'] = cim_battery.CycleCount
                        cycle_count_found = True
                        break
                
                # Method 2: Try root/wmi namespace for vendor-specific data
                if not cycle_count_found:
                    try:
                        wmi_namespace = wmi.WMI(namespace='root/wmi')
                        # Try different possible battery cycle count classes
                        for class_name in ['BatteryStatus', 'BattCycleCount', 'MSBattery_StaticData']:
                            try:
                                wmi_class = getattr(wmi_namespace, class_name, None)
                                if wmi_class:
                                    for item in wmi_class():
                                        # Look for cycle count in any available property
                                        for prop_name in ['CycleCount', 'BatteryCycleCount', 'CycleCount', 'Cycles']:
                                            if hasattr(item, prop_name):
                                                cycle_value = getattr(item, prop_name, None)
                                                if cycle_value is not None:
                                                    battery_info['cycle_count'] = cycle_value
                                                    cycle_count_found = True
                                                    break
                                        if cycle_count_found:
                                            break
                                if cycle_count_found:
                                    break
                            except:
                                continue
                    except:
                        pass
                
                # If cycle count not found, indicate it's not available
                if not cycle_count_found:
                    battery_info['cycle_count'] = 'Not Available'
                
                # Calculate battery health if we have capacity data
                if 'design_capacity' in battery_info and 'full_charge_capacity' in battery_info:
                    if battery_info['design_capacity'] > 0:
                        health_percentage = (battery_info['full_charge_capacity'] / battery_info['design_capacity']) * 100
                        battery_info['health_percentage'] = round(health_percentage, 1)
                
                # Check if this is a laptop
                for enclosure in c.Win32_SystemEnclosure():
                    if hasattr(enclosure, 'ChassisTypes') and enclosure.ChassisTypes:
                        # Chassis types for laptops: 8=Portable, 9=Laptop, 10=Notebook, 14=Sub Notebook, 30=Tablet, 31=Convertible, 32=Detachable
                        laptop_types = [8, 9, 10, 14, 30, 31, 32]
                        if any(chassis_type in laptop_types for chassis_type in enclosure.ChassisTypes):
                            battery_info['is_laptop'] = True
                        else:
                            battery_info['is_laptop'] = False
                    break
                
            except Exception as wmi_error:
                # If WMI fails, we still have basic psutil data
                battery_info['wmi_error'] = str(wmi_error)
                battery_info['cycle_count'] = 'Not Available'
            finally:
                try:
                    pythoncom.CoUninitialize()
                except:
                    pass
            
            if not battery_info:
                return {'status': 'No battery found'}
            
            return battery_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_other_info(self):
        """Get other system information including sensors, cameras, TPM, etc."""
        try:
            other_info = {}
            
            # Get sensors (temperatures, fan speeds, voltages)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    temp_list = []
                    for name, entries in temps.items():
                        for entry in entries:
                            if entry.current:
                                temp_list.append(f"{name}: {entry.current}°C")
                    other_info['temperatures'] = temp_list if temp_list else ['Not Available']
                else:
                    other_info['temperatures'] = ['Not Available']
                
                # Fan speeds
                fans = psutil.sensors_fans()
                if fans:
                    fan_list = []
                    for name, entries in fans.items():
                        for entry in entries:
                            if entry.current:
                                fan_list.append(f"{name}: {entry.current} RPM")
                    other_info['fan_speeds'] = fan_list if fan_list else ['Not Available']
                else:
                    other_info['fan_speeds'] = ['Not Available']
            except:
                other_info['temperatures'] = ['Not Available']
                other_info['fan_speeds'] = ['Not Available']
            
            # Get camera information using WMI
            try:
                import pythoncom
                pythoncom.CoInitialize()
                c = wmi.WMI()
                
                cameras = []
                for camera in c.Win32_PnPEntity():
                    if hasattr(camera, 'Name') and camera.Name:
                        name = camera.Name.upper()
                        if any(keyword in name for keyword in ['CAMERA', 'WEBCAM', 'VIDEO', 'IMAGING']):
                            cameras.append(camera.Name)
                
                other_info['cameras'] = cameras if cameras else ['No cameras detected']
                
                # Get TPM information
                tpm_info = []
                try:
                    for tpm in c.Win32_Tpm():
                        if hasattr(tpm, 'SpecVersion') and tpm.SpecVersion:
                            tpm_info.append(f"TPM {tpm.SpecVersion}")
                        elif hasattr(tpm, 'PhysicalPresenceVersionInfo'):
                            tpm_info.append("TPM Present")
                        break
                    
                    if not tpm_info:
                        # Try alternative method
                        for security in c.Win32_SystemEnclosure():
                            if hasattr(security, 'SecurityBreach'):
                                tpm_info.append("Security features present")
                                break
                        
                    other_info['tpm'] = tpm_info if tpm_info else ['TPM status unknown']
                except:
                    other_info['tpm'] = ['TPM status unknown']
                
                # Get chassis type (already doing this in battery, but let's get it here too)
                chassis_types = []
                for enclosure in c.Win32_SystemEnclosure():
                    if hasattr(enclosure, 'ChassisTypes') and enclosure.ChassisTypes:
                        chassis_map = {
                            1: 'Other', 2: 'Unknown', 3: 'Desktop', 4: 'Low Profile Desktop',
                            5: 'Pizza Box', 6: 'Mini Tower', 7: 'Tower', 8: 'Portable',
                            9: 'Laptop', 10: 'Notebook', 11: 'Hand Held', 12: 'Docking Station',
                            13: 'All In One', 14: 'Sub Notebook', 15: 'Space-saving',
                            16: 'Lunch Box', 17: 'Main Server Chassis', 18: 'Expansion Chassis',
                            19: 'SubChassis', 20: 'Bus Expansion Chassis', 21: 'Peripheral Chassis',
                            22: 'RAID Chassis', 23: 'Rack Mount Chassis', 24: 'Sealed-case PC',
                            25: 'Multi-system', 26: 'Compact PCI', 27: 'Advanced TCA', 28: 'Blade',
                            29: 'Blade Enclosure', 30: 'Tablet', 31: 'Convertible', 32: 'Detachable'
                        }
                        types = [chassis_map.get(ct, f'Unknown ({ct})') for ct in enclosure.ChassisTypes]
                        chassis_types.extend(types)
                    break
                
                other_info['chassis_type'] = chassis_types if chassis_types else ['Unknown']
                
                # Try to get Secure Boot status
                secure_boot = []
                try:
                    # This is a simplified check - actual secure boot requires more complex detection
                    for bios in c.Win32_BIOS():
                        if hasattr(bios, 'BIOSVersion'):
                            # Check if UEFI is mentioned in BIOS version (simplified check)
                            if 'UEFI' in str(bios.BIOSVersion).upper():
                                secure_boot.append('UEFI capable')
                            else:
                                secure_boot.append('Legacy BIOS')
                        break
                    
                    other_info['secure_boot'] = secure_boot if secure_boot else ['Status unknown']
                except:
                    other_info['secure_boot'] = ['Status unknown']
                
            except Exception as wmi_error:
                other_info['cameras'] = ['WMI error: Cannot detect cameras']
                other_info['tpm'] = ['WMI error: Cannot detect TPM']
                other_info['chassis_type'] = ['WMI error: Cannot detect chassis']
                other_info['secure_boot'] = ['WMI error: Cannot detect secure boot']
            finally:
                try:
                    pythoncom.CoUninitialize()
                except:
                    pass
            
            return other_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_all_info(self):
        """Get all hardware information"""
        return {
            'system': self.get_system_info(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'gpu': self.get_gpu_info(),
            'network': self.get_network_info(),
            'battery': self.get_battery_info(),
            'other': self.get_other_info(),
        }
    
    def _bytes_to_gb(self, bytes_value):
        """Convert bytes to GB"""
        try:
            return round(bytes_value / (1024**3), 2)
        except:
            return 0
    
    def _bytes_to_mb(self, bytes_value):
        """Convert bytes to MB"""
        try:
            return round(bytes_value / (1024**2), 2)
        except:
            return 0

# Test the module
if __name__ == "__main__":
    hw = HardwareInfo()
    print("Testing Hardware Info Module...")
    
    # Test each component
    print("\n=== CPU INFO ===")
    cpu_info = hw.get_cpu_info()
    for key, value in cpu_info.items():
        print(f"{key}: {value}")
    
    print("\n=== MEMORY INFO ===")
    memory_info = hw.get_memory_info()
    for key, value in memory_info.items():
        print(f"{key}: {value}")
    
    print("\n=== SYSTEM INFO ===")
    system_info = hw.get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")