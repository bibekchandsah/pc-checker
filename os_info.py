"""
Operating System Information Module
Collects detailed OS information and system configuration
"""

import platform
import subprocess
import os
import sys
import winreg
from datetime import datetime
import psutil

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

class OSInfo:
    def __init__(self):
        if WMI_AVAILABLE:
            try:
                self.wmi = wmi.WMI()
            except:
                self.wmi = None
        else:
            self.wmi = None
    
    def get_os_details(self):
        """Get detailed operating system information"""
        try:
            info = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'architecture': platform.architecture(),
                'platform': platform.platform(),
                'node': platform.node(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
                'uptime': str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())),
            }
            
            # Windows-specific information
            if platform.system().lower() == 'windows':
                info.update(self._get_windows_details())
            
            # Get environment variables
            info['environment_variables'] = dict(os.environ)
            
            # Get PATH variable
            info['path'] = os.environ.get('PATH', '').split(os.pathsep)
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def _get_windows_details(self):
        """Get Windows-specific details"""
        details = {}
        
        try:
            # Get Windows version from registry
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                              r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
                details['windows_product_name'] = winreg.QueryValueEx(key, "ProductName")[0]
                details['windows_version'] = winreg.QueryValueEx(key, "CurrentVersion")[0]
                try:
                    details['windows_build'] = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                except:
                    pass
                try:
                    details['windows_display_version'] = winreg.QueryValueEx(key, "DisplayVersion")[0]
                except:
                    pass
                try:
                    details['windows_edition'] = winreg.QueryValueEx(key, "EditionID")[0]
                except:
                    pass
                try:
                    details['windows_install_date'] = winreg.QueryValueEx(key, "InstallDate")[0]
                except:
                    pass
        except Exception as e:
            details['registry_error'] = str(e)
        
        # Get Windows information using WMI
        if self.wmi:
            try:
                for os_info in self.wmi.Win32_OperatingSystem():
                    details['windows_name'] = os_info.Name
                    details['windows_version_wmi'] = os_info.Version
                    details['windows_service_pack'] = os_info.ServicePackMajorVersion
                    details['windows_architecture'] = os_info.OSArchitecture
                    details['windows_install_date_wmi'] = os_info.InstallDate
                    details['windows_last_boot_time'] = os_info.LastBootUpTime
                    details['windows_total_memory'] = self._bytes_to_gb(int(os_info.TotalVisibleMemorySize) * 1024)
                    details['windows_free_memory'] = self._bytes_to_gb(int(os_info.FreePhysicalMemory) * 1024)
                    details['windows_serial_number'] = os_info.SerialNumber
                    details['windows_organization'] = os_info.Organization
                    details['windows_registered_user'] = os_info.RegisteredUser
                    break
            except Exception as e:
                details['wmi_os_error'] = str(e)
        
        return details
    
    def get_installed_software(self):
        """Get list of installed software"""
        software_list = []
        
        if platform.system().lower() == 'windows':
            software_list = self._get_windows_software()
        
        return software_list
    
    def _get_windows_software(self):
        """Get installed software on Windows"""
        software_list = []
        
        # Registry paths for installed software
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for registry_path in registry_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    software_info = {'name': display_name}
                                    
                                    try:
                                        software_info['version'] = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                    except:
                                        software_info['version'] = 'Unknown'
                                    
                                    try:
                                        software_info['publisher'] = winreg.QueryValueEx(subkey, "Publisher")[0]
                                    except:
                                        software_info['publisher'] = 'Unknown'
                                    
                                    try:
                                        software_info['install_date'] = winreg.QueryValueEx(subkey, "InstallDate")[0]
                                    except:
                                        software_info['install_date'] = 'Unknown'
                                    
                                    try:
                                        software_info['size'] = winreg.QueryValueEx(subkey, "EstimatedSize")[0]
                                    except:
                                        software_info['size'] = 'Unknown'
                                    
                                    software_list.append(software_info)
                                except FileNotFoundError:
                                    continue
                        except Exception:
                            continue
            except Exception as e:
                continue
        
        # Remove duplicates and sort
        unique_software = {}
        for software in software_list:
            key = software['name'].lower()
            if key not in unique_software:
                unique_software[key] = software
        
        return sorted(list(unique_software.values()), key=lambda x: x['name'].lower())
    
    def get_system_services(self):
        """Get system services information"""
        services = []
        
        if platform.system().lower() == 'windows' and self.wmi:
            try:
                for service in self.wmi.Win32_Service():
                    service_info = {
                        'name': service.Name,
                        'display_name': service.DisplayName,
                        'state': service.State,
                        'start_mode': service.StartMode,
                        'status': service.Status,
                        'path': service.PathName,
                        'description': service.Description,
                    }
                    services.append(service_info)
            except Exception as e:
                services = [{'error': str(e)}]
        
        return services
    
    def get_startup_programs(self):
        """Get startup programs"""
        startup_programs = []
        
        if platform.system().lower() == 'windows':
            startup_programs = self._get_windows_startup_programs()
        
        return startup_programs
    
    def _get_windows_startup_programs(self):
        """Get Windows startup programs"""
        startup_programs = []
        
        # Registry paths for startup programs
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        ]
        
        for hive, registry_path in registry_paths:
            try:
                with winreg.OpenKey(hive, registry_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_programs.append({
                                'name': name,
                                'command': value,
                                'location': f"{hive.name}\\{registry_path}"
                            })
                        except Exception:
                            continue
            except Exception:
                continue
        
        return startup_programs
    
    def get_system_drivers(self):
        """Get system drivers information"""
        drivers = []
        
        if platform.system().lower() == 'windows' and self.wmi:
            try:
                for driver in self.wmi.Win32_SystemDriver():
                    driver_info = {
                        'name': driver.Name,
                        'display_name': driver.DisplayName,
                        'state': driver.State,
                        'start_mode': driver.StartMode,
                        'status': driver.Status,
                        'path': driver.PathName,
                        'description': driver.Description,
                    }
                    drivers.append(driver_info)
            except Exception as e:
                drivers = [{'error': str(e)}]
        
        return drivers
    
    def get_users_and_groups(self):
        """Get users and groups information"""
        users_groups = {}
        
        if platform.system().lower() == 'windows' and self.wmi:
            try:
                # Get users
                users = []
                for user in self.wmi.Win32_UserAccount():
                    user_info = {
                        'name': user.Name,
                        'full_name': user.FullName,
                        'description': user.Description,
                        'disabled': user.Disabled,
                        'local_account': user.LocalAccount,
                        'lockout': user.Lockout,
                        'password_changeable': user.PasswordChangeable,
                        'password_expires': user.PasswordExpires,
                        'password_required': user.PasswordRequired,
                        'sid': user.SID,
                    }
                    users.append(user_info)
                users_groups['users'] = users
                
                # Get groups
                groups = []
                for group in self.wmi.Win32_Group():
                    group_info = {
                        'name': group.Name,
                        'description': group.Description,
                        'local_account': group.LocalAccount,
                        'sid': group.SID,
                    }
                    groups.append(group_info)
                users_groups['groups'] = groups
                
            except Exception as e:
                users_groups = {'error': str(e)}
        
        return users_groups
    
    def get_network_configuration(self):
        """Get network configuration"""
        network_config = {}
        
        if platform.system().lower() == 'windows' and self.wmi:
            try:
                # Get network adapters
                adapters = []
                for adapter in self.wmi.Win32_NetworkAdapterConfiguration():
                    if adapter.IPEnabled:
                        adapter_info = {
                            'description': adapter.Description,
                            'ip_addresses': adapter.IPAddress,
                            'subnet_masks': adapter.IPSubnet,
                            'default_gateways': adapter.DefaultIPGateway,
                            'dns_servers': adapter.DNSServerSearchOrder,
                            'dhcp_enabled': adapter.DHCPEnabled,
                            'dhcp_server': adapter.DHCPServer,
                            'mac_address': adapter.MACAddress,
                            'wins_servers': adapter.WINSPrimaryServer,
                        }
                        adapters.append(adapter_info)
                network_config['adapters'] = adapters
                
            except Exception as e:
                network_config = {'error': str(e)}
        
        return network_config
    
    def get_all_os_info(self):
        """Get all OS information"""
        return {
            'os_details': self.get_os_details(),
            'installed_software': self.get_installed_software(),
            'system_services': self.get_system_services(),
            'startup_programs': self.get_startup_programs(),
            'system_drivers': self.get_system_drivers(),
            'users_and_groups': self.get_users_and_groups(),
            'network_configuration': self.get_network_configuration(),
        }
    
    def _bytes_to_gb(self, bytes_value):
        """Convert bytes to GB"""
        try:
            return round(bytes_value / (1024**3), 2)
        except:
            return 0

# Test the module
if __name__ == "__main__":
    os_info = OSInfo()
    print("Testing OS Info Module...")
    
    print("\n=== OS DETAILS ===")
    os_details = os_info.get_os_details()
    for key, value in os_details.items():
        if key != 'environment_variables' and key != 'path':
            print(f"{key}: {value}")
    
    print(f"\nPath entries: {len(os_details.get('path', []))}")
    print(f"Environment variables: {len(os_details.get('environment_variables', {}))}")