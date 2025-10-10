"""
Subprocess Helper Module
Provides utilities for running subprocess commands without showing terminal windows on Windows
"""

import subprocess
import sys
import platform

# Windows-specific constants for hiding console windows
if platform.system() == 'Windows':
    import ctypes
    from ctypes import wintypes
    
    # Constants for CREATE_NO_WINDOW
    CREATE_NO_WINDOW = 0x08000000
    DETACHED_PROCESS = 0x00000008
    
    # startupinfo to hide console window
    def get_startup_info():
        """Get startup info to hide console window"""
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0  # SW_HIDE
        return startupinfo
else:
    CREATE_NO_WINDOW = 0
    DETACHED_PROCESS = 0
    
    def get_startup_info():
        """Return None for non-Windows systems"""
        return None


def run_hidden(cmd, **kwargs):
    """
    Run a subprocess command without showing a terminal window
    
    Args:
        cmd: Command to run (string or list)
        **kwargs: Additional arguments to pass to subprocess.run()
    
    Returns:
        subprocess.CompletedProcess object
    """
    if platform.system() == 'Windows':
        # Combine flags to ensure no window is created
        existing_flags = kwargs.get('creationflags', 0)
        kwargs['creationflags'] = existing_flags | CREATE_NO_WINDOW
        
        # Always set startupinfo to hide window
        if 'startupinfo' not in kwargs:
            kwargs['startupinfo'] = get_startup_info()
    
    return subprocess.run(cmd, **kwargs)


def check_output_hidden(cmd, **kwargs):
    """
    Run a subprocess command and capture output without showing a terminal window
    
    Args:
        cmd: Command to run (string or list)
        **kwargs: Additional arguments to pass to subprocess.check_output()
    
    Returns:
        bytes: Output from the command
    """
    if platform.system() == 'Windows':
        # Combine flags to ensure no window is created
        existing_flags = kwargs.get('creationflags', 0)
        kwargs['creationflags'] = existing_flags | CREATE_NO_WINDOW
        
        # Always set startupinfo to hide window
        if 'startupinfo' not in kwargs:
            kwargs['startupinfo'] = get_startup_info()
    
    return subprocess.check_output(cmd, **kwargs)


def Popen_hidden(cmd, **kwargs):
    """
    Create a subprocess.Popen object without showing a terminal window
    
    Args:
        cmd: Command to run (string or list)
        **kwargs: Additional arguments to pass to subprocess.Popen()
    
    Returns:
        subprocess.Popen object
    """
    if platform.system() == 'Windows':
        # Combine flags to ensure no window is created
        existing_flags = kwargs.get('creationflags', 0)
        kwargs['creationflags'] = existing_flags | CREATE_NO_WINDOW
        
        # Always set startupinfo to hide window
        if 'startupinfo' not in kwargs:
            kwargs['startupinfo'] = get_startup_info()
    
    return subprocess.Popen(cmd, **kwargs)


def call_hidden(cmd, **kwargs):
    """
    Run a subprocess.call command without showing a terminal window
    
    Args:
        cmd: Command to run (string or list)
        **kwargs: Additional arguments to pass to subprocess.call()
    
    Returns:
        int: Return code from the command
    """
    if platform.system() == 'Windows':
        # Combine flags to ensure no window is created
        existing_flags = kwargs.get('creationflags', 0)
        kwargs['creationflags'] = existing_flags | CREATE_NO_WINDOW
        
        # Always set startupinfo to hide window
        if 'startupinfo' not in kwargs:
            kwargs['startupinfo'] = get_startup_info()
    
    return subprocess.call(cmd, **kwargs)
