#!/usr/bin/env python3
"""
Smart File Organizer - GUI Launcher
This script launches the GUI interface directly when the executable is double-clicked.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Main entry point for the GUI launcher"""
    try:
        # Import the GUI main window
        from gui.main_window import SmartFileOrganizerGUI
        
        # Create and run the GUI
        root = tk.Tk()
        app = SmartFileOrganizerGUI(root)
        root.mainloop()
        
    except ImportError as e:
        # Handle import errors gracefully
        error_msg = f"Error importing required modules: {e}\n\nPlease ensure all dependencies are installed."
        if 'tkinter' in str(e).lower():
            error_msg = "Tkinter is not available on this system.\n\nThis application requires a GUI environment."
        
        # Show error in console if GUI fails
        print(f"ERROR: {error_msg}")
        input("Press Enter to exit...")
        sys.exit(1)
        
    except Exception as e:
        # Handle any other errors
        error_msg = f"An unexpected error occurred: {e}"
        print(f"ERROR: {error_msg}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
