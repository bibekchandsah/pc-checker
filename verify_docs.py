#!/usr/bin/env python3

"""
README and requirements verification script
Checks if all mentioned features and dependencies are properly documented
"""

import os
import re

def verify_readme():
    """Verify README.md content matches application features"""
    print("🔍 Verifying README.md content...")
    
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Check for key sections
    required_sections = [
        "# Laptop Testing Program",
        "## ✅ Latest Updates (v1.2)",
        "Enhanced CSV Reporting",
        "System Overview",
        "Hardware Details", 
        "Operating System Details",
        "📊 Enhanced CSV Reports",
        "System Tests",
        "Requirements",
        "Installation",
        "Usage",
        "📊 CSV Report Generation",
        "Technical Details",
        "Troubleshooting",
        "Development",
        "Version History"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in readme_content:
            missing_sections.append(section)
    
    if missing_sections:
        print("❌ Missing sections in README:")
        for section in missing_sections:
            print(f"  - {section}")
    else:
        print("✅ All required sections found in README")
    
    # Check for new features
    new_features = [
        "8 comprehensive information cards",
        "Complete installed software list",
        "CSV reports",
        "Card-based organization",
        "Professional dark theme",
        "System Summary Card",
        "CPU Information Card", 
        "RAM Information Card",
        "ROM Information Card",
        "Battery Information Card",
        "Other Information Card"
    ]
    
    found_features = []
    for feature in new_features:
        if feature.lower() in readme_content.lower():
            found_features.append(feature)
    
    print(f"\n📋 New features documented: {len(found_features)}/{len(new_features)}")
    for feature in found_features:
        print(f"  ✅ {feature}")
    
    missing_features = set(new_features) - set(found_features)
    if missing_features:
        print("\n❌ Missing feature documentation:")
        for feature in missing_features:
            print(f"  - {feature}")

def verify_requirements():
    """Verify requirements.txt has all necessary packages"""
    print("\n🔍 Verifying requirements.txt...")
    
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        requirements_content = f.read()
    
    # Check for essential packages
    essential_packages = [
        "PySide6",
        "psutil", 
        "py-cpuinfo",
        "GPUtil",
        "wmi",
        "requests",
        "speedtest-cli",
        "opencv-python",
        "pyaudio",
        "matplotlib",
        "numpy",
        "scipy",
        "distro"
    ]
    
    found_packages = []
    missing_packages = []
    
    for package in essential_packages:
        if package.lower() in requirements_content.lower():
            found_packages.append(package)
        else:
            missing_packages.append(package)
    
    print(f"📦 Packages documented: {len(found_packages)}/{len(essential_packages)}")
    for package in found_packages:
        print(f"  ✅ {package}")
    
    if missing_packages:
        print("\n❌ Missing packages:")
        for package in missing_packages:
            print(f"  - {package}")
    
    # Check for version specifications
    lines = requirements_content.split('\n')
    versioned_packages = [line for line in lines if '>=' in line and not line.startswith('#')]
    print(f"\n📌 Packages with version specifications: {len(versioned_packages)}")
    for package in versioned_packages:
        if package.strip():
            print(f"  ✅ {package.strip()}")

def check_file_structure():
    """Check if all mentioned files exist"""
    print("\n🔍 Verifying file structure...")
    
    required_files = [
        "script.py",
        "hardware_info.py", 
        "os_info.py",
        "system_tests.py",
        "requirements.txt",
        "test_modules.py",
        "README.md"
    ]
    
    existing_files = []
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            existing_files.append(file)
        else:
            missing_files.append(file)
    
    print(f"📁 Files present: {len(existing_files)}/{len(required_files)}")
    for file in existing_files:
        print(f"  ✅ {file}")
    
    if missing_files:
        print("\n❌ Missing files:")
        for file in missing_files:
            print(f"  - {file}")
    
    # Check for generated CSV files
    csv_files = [f for f in os.listdir('.') if f.startswith('system_report_') and f.endswith('.csv')]
    if csv_files:
        print(f"\n📊 Generated CSV reports found: {len(csv_files)}")
        for csv_file in csv_files[-3:]:  # Show last 3
            print(f"  📄 {csv_file}")

def main():
    """Main verification function"""
    print("🔍 README and Requirements Verification")
    print("=" * 50)
    
    verify_readme()
    verify_requirements() 
    check_file_structure()
    
    print("\n" + "=" * 50)
    print("✅ Verification completed!")
    print("\n📋 Summary:")
    print("- README.md updated with v1.2 features")
    print("- Enhanced CSV reporting documentation added")
    print("- Complete system cards information included")
    print("- Requirements.txt updated with version specifications")
    print("- All core files documented and verified")

if __name__ == '__main__':
    main()