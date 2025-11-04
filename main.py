#!/usr/bin/env python3
"""
Smart File Organizer - Main Entry Point
A clean, modern file organization tool with CLI and GUI interfaces.
"""

import sys
import argparse
from pathlib import Path

def run_cli(args):
    """Run the CLI interface"""
    from cli.main import main as cli_main
    
    # Set up sys.argv for the CLI module
    sys.argv = [sys.argv[0]]
    if args.path:
        sys.argv.extend(["--path", args.path])
    if args.mode:
        sys.argv.extend(["--mode", args.mode])
    if args.profile:
        sys.argv.extend(["--profile", args.profile])
    if args.dry_run:
        sys.argv.append("--dry-run")
    if args.config:
        sys.argv.extend(["--config", args.config])
    
    cli_main()

def run_gui():
    """Run the GUI interface"""
    try:
        from gui.main_window import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)

def run_monitor(args):
    """Run the file monitor"""
    if not args.path:
        print("Error: --path is required for monitor mode")
        sys.exit(1)
    
    try:
        from core.file_monitor import FileMonitor
        from core.file_organizer import FileOrganizer
        
        print(f"Starting file monitoring for: {args.path}")
        print("Press Ctrl+C to stop monitoring")
        
        organizer = FileOrganizer(args.config) if args.config else FileOrganizer()
        monitor = FileMonitor(organizer, organizer.config)
        monitor.add_watch(args.path)
        monitor.start_monitoring()
        
        # Keep running until interrupted
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping file monitoring...")
            monitor.stop_monitoring()
            print("File monitoring stopped")
            
    except ImportError as e:
        print(f"Error: Monitor dependencies not available: {e}")
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Smart File Organizer - Clean and simple file organization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --gui                    # Launch GUI interface
  %(prog)s --cli --path Downloads   # Organize Downloads folder
  %(prog)s --monitor --path Desktop # Monitor Desktop for changes
        """
    )
    
    # Interface selection (mutually exclusive)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--cli", action="store_true", help="Command-line interface")
    group.add_argument("--gui", action="store_true", help="Graphical interface (default)")
    group.add_argument("--monitor", action="store_true", help="File monitoring mode")
    
    # Common options
    parser.add_argument("--path", "-p", help="Folder path to organize/monitor")
    parser.add_argument("--mode", "-m", choices=["type", "size", "date", "content"], 
                       default="type", help="Organization mode")
    parser.add_argument("--profile", "-pr", choices=["default", "work", "personal"], 
                       default="default", help="Configuration profile")
    parser.add_argument("--dry-run", "-d", action="store_true", 
                       help="Preview changes without moving files")
    parser.add_argument("--config", "-c", help="Custom configuration file path")
    
    args = parser.parse_args()
    
    # Route to appropriate interface
    if args.cli:
        run_cli(args)
    elif args.gui:
        run_gui()
    elif args.monitor:
        run_monitor(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
