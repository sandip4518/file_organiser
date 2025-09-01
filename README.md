# Smart File Organizer 🚀

**Advanced productivity tool for organizing files with AI-powered categorization, rules engine, and multiple interfaces**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/yourusername/smart-file-organizer)

## ✨ Features

### 🎯 Core Organization
- **Multiple Sorting Modes**: By type, size, date, and content analysis
- **Smart Categorization**: Predefined categories for Images, Documents, Audio, Video, Archives, Code, and Executables
- **Custom Rules Engine**: Define complex organization rules (e.g., "move PDFs > 10MB to Large_PDFs")
- **Duplicate Handling**: Automatic duplicate detection and renaming
- **Cross-platform Support**: Works on Windows, macOS, and Linux

### 🚀 Advanced Features
- **AI-Powered Content Analysis**: Detect file content beyond just extensions
- **Real-time Monitoring**: Auto-organize new files using watchdog
- **Scheduled Organization**: Daily, weekly, and monthly automated runs
- **Multiple Profiles**: Work, personal, and custom profiles with different rules
- **Backup & Safety**: Backup mode, archive old files, and undo functionality

### 🖥️ Multiple Interfaces
- **Rich CLI**: Colorful command-line interface with progress bars
- **Modern GUI**: Tkinter-based graphical interface with drag-and-drop
- **File Monitor**: Background service for continuous organization
- **Portable EXE**: Standalone executable (no Python installation required)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-file-organizer.git
   cd smart-file-organizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # CLI Mode
   python main.py --cli --path "C:\Users\Username\Downloads"
   
   # GUI Mode
   python main.py --gui
   
   # Monitor Mode
   python main.py --monitor --path "C:\Users\Username\Downloads"
   ```

## 📖 Usage Examples

### Command Line Interface

```bash
# Basic organization by file type
python main.py --cli --path "C:\Users\Username\Downloads"

# Organize by file size
python main.py --cli --path "C:\Users\Username\Downloads" --mode size

# Use work profile with dry run
python main.py --cli --path "C:\Users\Username\Downloads" --profile work --dry-run

# Custom configuration file
python main.py --cli --path "C:\Users\Username\Downloads" --config "my_config.yaml"

# Undo last operation
python main.py --cli --undo
```

### GUI Interface

```bash
# Launch graphical interface
python main.py --gui
```

The GUI provides:
- Folder picker with drag-and-drop support
- Real-time progress tracking
- Live logs and status updates
- Profile and mode selection
- Dry run preview mode

### File Monitoring

```bash
# Start real-time monitoring
python main.py --monitor --path "C:\Users\Username\Downloads"
```

This will:
- Watch the specified folder for new files
- Automatically organize new files as they appear
- Run in the background until stopped (Ctrl+C)

## ⚙️ Configuration

### Default Configuration

The application comes with a comprehensive default configuration in `config/default_config.yaml`:

```yaml
# File Categories
categories:
  Images:
    extensions: [jpg, jpeg, png, gif, bmp, svg, webp, tiff, ico]
    folder_name: "Images"
    
  Documents:
    extensions: [pdf, docx, txt, pptx, xlsx, csv, md, rtf, odt, odp, ods]
    folder_name: "Documents"

# Custom Rules
rules:
  - name: "Large PDFs"
    condition: "extension == 'pdf' and size > 10485760"  # 10MB
    action: "move_to_folder"
    target: "Large_PDFs"
    
  - name: "Screenshots"
    condition: "filename_contains('screenshot') or filename_contains('screencap')"
    action: "move_to_folder"
    target: "Screenshots"

# Profiles
profiles:
  default:
    enabled_categories: ["Images", "Documents", "Audio", "Video", "Archives", "Code", "Executables"]
    rules: ["Large PDFs", "Screenshots", "Invoices", "Old Files"]
    
  work:
    enabled_categories: ["Documents", "Code", "Archives"]
    rules: ["Large PDFs", "Invoices"]
```

### Custom Configuration

1. Copy `config/default_config.yaml` to `config/config.yaml`
2. Modify the settings according to your needs
3. Use `--config config/config.yaml` when running the application

## 🔧 Advanced Features

### Rules Engine

The rules engine supports complex conditions:

```yaml
rules:
  - name: "Work Documents"
    condition: "extension == 'pdf' and filename_contains('report') and modified_days_ago < 30"
    action: "move_to_folder"
    target: "Work_Reports"
    
  - name: "Old Archives"
    condition: "extension in ['zip', 'rar', '7z'] and modified_days_ago > 365"
    action: "move_to_folder"
    target: "Old_Archives"
```

### Content Analysis

The content analysis mode can detect file content:

- **Text Files**: Keyword detection for invoices, resumes, etc.
- **Images**: Basic metadata analysis
- **Documents**: Content-based categorization

### Scheduling

Configure automatic organization:

```yaml
schedule:
  daily: true
  daily_time: "02:00"
  weekly: true
  weekly_day: "sunday"
  weekly_time: "03:00"
  monthly: true
  monthly_day: 1
  monthly_time: "04:00"

scheduled_paths:
  - "C:\\Users\\Username\\Downloads"
  - "C:\\Users\\Username\\Desktop"

scheduled_mode: "type"
scheduled_profile: "default"
```

## 🏗️ Building Standalone Executable

### Using PyInstaller

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**
   ```bash
   # Using the spec file
   pyinstaller build_exe.spec
   
   # Or direct command
   pyinstaller --onefile --windowed --add-data "config;config" --add-data "core;core" --add-data "cli;cli" --add-data "gui;gui" main.py
   ```

3. **Find the executable**
   - Console version: `dist/SmartFileOrganizer.exe`
   - GUI version: `dist/SmartFileOrganizer_GUI.exe`

### Distribution

The standalone executable includes:
- All Python dependencies
- Configuration files
- Core modules
- No Python installation required

## 📁 Project Structure

```
smart-file-organizer/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── build_exe.spec         # PyInstaller configuration
├── README.md              # This file
├── config/
│   └── default_config.yaml # Default configuration
├── core/
│   ├── file_organizer.py  # Core organization logic
│   └── file_monitor.py    # File monitoring system
├── cli/
│   └── main.py            # Command-line interface
└── gui/
    └── main_window.py     # Graphical user interface
```

## 🚨 Safety Features

### Data Protection
- **Backup Mode**: Copy files before organizing
- **Dry Run**: Preview changes without moving files
- **Undo Functionality**: Revert last organization operation
- **Operation Logging**: Complete history of all operations

### Error Handling
- **Graceful Failures**: Continue processing other files on errors
- **Detailed Logging**: Comprehensive error reporting
- **Validation**: Path and permission checking

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission Errors**
   - Run as administrator (Windows)
   - Check folder permissions
   - Ensure write access to target directories

3. **Configuration Issues**
   - Verify YAML syntax
   - Check file paths in configuration
   - Use absolute paths for critical directories

### Logs

- **Application Log**: `organizer.log`
- **Operation History**: `operation_history.json`
- **Console Output**: Rich formatted output with error details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal output
- [Watchdog](https://github.com/gorakhargosh/watchdog) - File system monitoring
- [PyYAML](https://github.com/yaml/pyyaml) - YAML parsing
- [PyInstaller](https://github.com/pyinstaller/pyinstaller) - Executable creation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/smart-file-organizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/smart-file-organizer/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/smart-file-organizer/wiki)

---

**Made with ❤️ for productivity enthusiasts everywhere**
