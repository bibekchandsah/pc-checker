"""
Build script for Laptop Testing Program
Compiles the application to a standalone .exe file using PyInstaller
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_directories():
    """Clean up old build directories"""
    print("🧹 Cleaning old build directories...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   ✓ Removed {dir_name}/")
            except Exception as e:
                print(f"   ✗ Could not remove {dir_name}/: {e}")

def build_exe():
    """Build the executable using PyInstaller"""
    print("\n🔨 Building executable...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    script_path = current_dir / "script.py"
    icon_path = current_dir / "icon.ico"
    
    # Check if required files exist
    if not script_path.exists():
        print(f"❌ Error: script.py not found at {script_path}")
        return False
    
    # PyInstaller command with all necessary options
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create a single executable file
        '--windowed',                   # No console window (GUI application)
        '--name=LaptopTestingProgram',  # Name of the executable
        '--clean',                      # Clean cache before building
    ]
    
    # Add icon if it exists
    if icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])
        print(f"   ℹ Using icon: {icon_path}")
    else:
        print(f"   ⚠ Warning: icon.ico not found at {icon_path}")
    
    # Add hidden imports for modules that might not be detected
    hidden_imports = [
        'hardware_info',
        'os_info',
        'system_tests',
        'update_manager',
        'window_utils',
        'subprocess_helper',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ]
    
    for module in hidden_imports:
        cmd.extend(['--hidden-import', module])
    
    # Exclude conflicting Qt bindings
    excluded_modules = [
        'PyQt5',
        'PyQt6',
        'tkinter',
        'kivy',
        'kivymd',
    ]
    
    for module in excluded_modules:
        cmd.extend(['--exclude-module', module])
    
    # Add data files
    data_files = [
        ('icon.png', '.'),
        ('icon.ico', '.'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ]
    
    for src, dest in data_files:
        src_path = current_dir / src
        if src_path.exists():
            cmd.extend(['--add-data', f'{src};{dest}'])
            print(f"   ℹ Adding data file: {src}")
    
    # Add the main script
    cmd.append(str(script_path))
    
    print(f"\n📦 Running PyInstaller with command:")
    print(f"   {' '.join(cmd)}\n")
    
    # Run PyInstaller
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print("\n✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False

def show_results():
    """Show the build results"""
    dist_dir = Path('dist')
    if dist_dir.exists():
        exe_file = dist_dir / 'LaptopTestingProgram.exe'
        if exe_file.exists():
            size_mb = exe_file.stat().st_size / (1024 * 1024)
            print(f"\n🎉 Executable created successfully!")
            print(f"   📁 Location: {exe_file.absolute()}")
            print(f"   📊 Size: {size_mb:.2f} MB")
            print(f"\n💡 You can now distribute this .exe file to users.")
            print(f"   Users don't need Python installed to run it!")
        else:
            print(f"\n⚠ Warning: dist/ directory exists but .exe file not found")
    else:
        print(f"\n⚠ Warning: dist/ directory not found")

def main():
    """Main build function"""
    print("=" * 60)
    print("  Laptop Testing Program - EXE Builder")
    print("=" * 60)
    
    # Ask user if they want to clean old builds
    response = input("\n🗑️  Clean old build directories? (y/n, default: y): ").strip().lower()
    if response in ['', 'y', 'yes']:
        clean_build_directories()
    
    # Build the executable
    success = build_exe()
    
    if success:
        show_results()
        print("\n" + "=" * 60)
        print("  Build process completed!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("  Build process failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
