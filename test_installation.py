#!/usr/bin/env python3
"""
Test script to verify Smart File Organizer installation
Run this script to check if all dependencies and modules are working correctly
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            module = importlib.import_module(module_name, package_name)
        else:
            module = importlib.import_module(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - ERROR: {e}")
        return False

def test_file_exists(file_path, description):
    """Test if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description} - OK")
        return True
    else:
        print(f"❌ {description} - MISSING: {file_path}")
        return False

def main():
    """Main test function"""
    print("🔍 Testing Smart File Organizer Installation")
    print("=" * 50)
    
    # Test Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - OK")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Python 3.8+ required")
        return False
    
    print("\n📦 Testing Dependencies:")
    print("-" * 30)
    
    # Test required packages
    required_packages = [
        'rich',
        'watchdog',
        'yaml',
        'pathlib',
        'tkinter',
    ]
    
    all_packages_ok = True
    for package in required_packages:
        if not test_import(package):
            all_packages_ok = False
    
    print("\n📁 Testing Project Files:")
    print("-" * 30)
    
    # Test project structure
    required_files = [
        ('main.py', 'Main entry point'),
        ('requirements.txt', 'Dependencies file'),
        ('config/default_config.yaml', 'Default configuration'),
        ('core/file_organizer.py', 'Core organizer module'),
        ('core/file_monitor.py', 'File monitor module'),
        ('cli/main.py', 'CLI interface'),
        ('gui/main_window.py', 'GUI interface'),
        ('README.md', 'Documentation'),
    ]
    
    all_files_ok = True
    for file_path, description in required_files:
        if not test_file_exists(file_path, description):
            all_files_ok = False
    
    print("\n🔧 Testing Core Modules:")
    print("-" * 30)
    
    # Test core module imports
    try:
        sys.path.append(str(Path(__file__).parent))
        from core.file_organizer import FileOrganizer
        print("✅ FileOrganizer class - OK")
        
        from core.file_monitor import FileMonitor
        print("✅ FileMonitor class - OK")
        
    except ImportError as e:
        print(f"❌ Core modules - FAILED: {e}")
        all_files_ok = False
    except Exception as e:
        print(f"⚠️  Core modules - ERROR: {e}")
        all_files_ok = False
    
    print("\n📊 Test Results:")
    print("-" * 30)
    
    if all_packages_ok and all_files_ok:
        print("🎉 All tests passed! Smart File Organizer is ready to use.")
        print("\n🚀 Quick start:")
        print("  CLI Mode: python main.py --cli --path \"C:\\Users\\Username\\Downloads\"")
        print("  GUI Mode: python main.py --gui")
        print("  Monitor Mode: python main.py --monitor --path \"C:\\Users\\Username\\Downloads\"")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Check file paths and permissions")
        print("  3. Ensure Python 3.8+ is installed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
