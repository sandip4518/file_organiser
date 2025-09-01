#!/usr/bin/env python3
"""
Smart File Organizer - Main Entry Point
Advanced productivity tool for organizing files with multiple interfaces
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main entry point for the Smart File Organizer"""
    parser = argparse.ArgumentParser(
        description="Smart File Organizer - Advanced productivity tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --cli --path "C:\\Users\\Username\\Downloads"
  %(prog)s --gui
  %(prog)s --monitor --path "C:\\Users\\Username\\Downloads"
        """
    )
    
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in command-line interface mode"
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Run in graphical user interface mode"
    )
    
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Run in file monitoring mode"
    )
    
    parser.add_argument(
        "--path", "-p",
        type=str,
        help="Path to the folder to organize (for CLI and monitor modes)"
    )
    
    parser.add_argument(
        "--mode", "-m",
        choices=["type", "size", "date", "content"],
        default="type",
        help="Sorting mode (default: type)"
    )
    
    parser.add_argument(
        "--profile", "-pr",
        choices=["default", "work", "personal"],
        default="default",
        help="Configuration profile (default: default)"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Show organization plan without moving files"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to custom configuration file"
    )
    
    args = parser.parse_args()
    
    # If no interface specified, show help
    if not any([args.cli, args.gui, args.monitor]):
        parser.print_help()
        return
    
    # CLI Mode
    if args.cli:
        from cli.main import main as cli_main
        # Set sys.argv for CLI
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
        return
    
    # GUI Mode
    if args.gui:
        try:
            from gui.main_window import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"Error importing GUI modules: {e}")
            print("Make sure all dependencies are installed: pip install -r requirements.txt")
            sys.exit(1)
        return
    
    # Monitor Mode
    if args.monitor:
        if not args.path:
            print("Error: --path is required for monitor mode")
            sys.exit(1)
        
        try:
            from core.file_monitor import FileMonitor
            from core.file_organizer import FileOrganizer
            
            print(f"Starting file monitoring for: {args.path}")
            print("Press Ctrl+C to stop monitoring")
            
            # Initialize organizer and monitor
            organizer = FileOrganizer(args.config) if args.config else FileOrganizer()
            monitor = FileMonitor(organizer, organizer.config)
            
            # Add watch path
            monitor.add_watch(args.path)
            
            # Start monitoring
            monitor.start_monitoring()
            
            # Keep running
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping file monitoring...")
                monitor.stop_monitoring()
                print("File monitoring stopped")
            
        except ImportError as e:
            print(f"Error importing monitor modules: {e}")
            print("Make sure all dependencies are installed: pip install -r requirements.txt")
            sys.exit(1)
        except Exception as e:
            print(f"Error in monitor mode: {e}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
