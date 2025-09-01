# Smart File Organizer - Installation & Usage Guide

## 🚀 Quick Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download
```bash
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python test_installation.py
```

## 🎯 Usage Modes

### 1. Command Line Interface (CLI)
**Best for:** Scripting, automation, server environments

```bash
# Basic organization by file type
python main.py --cli --path "C:\Users\Username\Downloads"

# Organize by file size
python main.py --cli --path "C:\Users\Username\Downloads" --mode size

# Use work profile with dry run (preview only)
python main.py --cli --path "C:\Users\Username\Downloads" --profile work --dry-run

# Custom configuration
python main.py --cli --path "C:\Users\Username\Downloads" --config "my_config.yaml"

# Undo last operation
python main.py --cli --undo
```

### 2. Graphical User Interface (GUI)
**Best for:** Desktop users, visual feedback, drag-and-drop

```bash
python main.py --gui
```

**GUI Features:**
- Folder picker with browse button
- Drag-and-drop folder support
- Real-time progress tracking
- Live logs and status updates
- Profile and mode selection
- Dry run preview mode

### 3. File Monitoring Mode
**Best for:** Continuous organization, background service

```bash
python main.py --monitor --path "C:\Users\Username\Downloads"
```

**Monitor Features:**
- Watches folder for new files
- Auto-organizes files as they appear
- Runs continuously until stopped (Ctrl+C)
- Logs all activities

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
2. Modify settings according to your needs
3. Use `--config config/config.yaml` when running

## 🔧 Advanced Features

### Rules Engine
Create complex organization rules:

```yaml
rules:
  - name: "Work Reports"
    condition: "extension == 'pdf' and filename_contains('report') and modified_days_ago < 30"
    action: "move_to_folder"
    target: "Work_Reports"
    
  - name: "Old Archives"
    condition: "extension in ['zip', 'rar', '7z'] and modified_days_ago > 365"
    action: "move_to_folder"
    target: "Old_Archives"
```

### Content Analysis Mode
Detect file content beyond extensions:

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

scheduled_paths:
  - "C:\\Users\\Username\\Downloads"
  - "C:\\Users\\Username\\Desktop"
```

## 🏗️ Building Standalone Executable

### Using PyInstaller

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build using spec file**
   ```bash
   pyinstaller build_exe.spec
   ```

3. **Or build directly**
   ```bash
   pyinstaller --onefile --windowed --add-data "config;config" --add-data "core;core" --add-data "cli;cli" --add-data "gui;gui" main.py
   ```

4. **Find executables**
   - Console version: `dist/SmartFileOrganizer.exe`
   - GUI version: `dist/SmartFileOrganizer_GUI.exe`

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

### Logs and Debugging

- **Application Log**: `organizer.log`
- **Operation History**: `operation_history.json`
- **Console Output**: Rich formatted output with error details

## 📱 Platform-Specific Notes

### Windows
- Use backslashes in paths: `C:\Users\Username\Downloads`
- Run as administrator for system folders
- Use `--monitor` mode for background service

### macOS
- Use forward slashes in paths: `/Users/username/Downloads`
- May need to grant accessibility permissions
- GUI works well with native look and feel

### Linux
- Use forward slashes in paths: `/home/username/Downloads`
- Install tkinter: `sudo apt-get install python3-tk`
- Monitor mode works well as systemd service

## 🎯 Use Cases

### Personal Use
- Organize Downloads folder
- Sort photos and documents
- Clean up Desktop
- Archive old files

### Work Environment
- Organize project files
- Sort client documents
- Manage code repositories
- Archive completed projects

### Server/Backup
- Monitor upload folders
- Organize backup files
- Sort log files
- Automated maintenance

## 🔄 Automation Examples

### Windows Task Scheduler
1. Create a batch file: `organize_downloads.bat`
   ```batch
   cd /d "C:\path\to\smart-file-organizer"
   python main.py --cli --path "C:\Users\Username\Downloads" --profile personal
   ```

2. Schedule to run daily at 2 AM

### Linux/macOS Cron
```bash
# Add to crontab (crontab -e)
0 2 * * * cd /path/to/smart-file-organizer && python main.py --cli --path "/home/username/Downloads" --profile personal
```

### Continuous Monitoring
```bash
# Start monitoring service
python main.py --monitor --path "C:\Users\Username\Downloads" --profile default
```

## 📊 Performance Tips

### Large Folders
- Use `--dry-run` first to preview
- Consider organizing in batches
- Use appropriate profiles for different content types

### Network Drives
- Ensure stable network connection
- Use local profiles for better performance
- Consider backup mode for important files

### Memory Usage
- Monitor memory usage with large operations
- Close other applications during large organization tasks
- Use appropriate sorting modes for your needs

---

**Need Help?** Check the main README.md or create an issue on GitHub!
