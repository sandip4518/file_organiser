#!/usr/bin/env python3
"""
Smart File Organizer GUI Interface
Provides a modern graphical interface using Tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
from pathlib import Path
import sys
import os

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.file_organizer import FileOrganizer

class SmartFileOrganizerGUI:
    """Main GUI window for the Smart File Organizer"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer - Advanced Productivity Tool")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize organizer
        self.organizer = FileOrganizer()
        self.selected_folder = None
        self.message_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        self.setup_styles()
        self.setup_bindings()
        
        # Start message processing
        self.process_messages()
    
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        
        # Configure styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Smart File Organizer", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Folder selection section
        self.setup_folder_selection(main_frame)
        
        # Options section
        self.setup_options_section(main_frame)
        
        # Action buttons
        self.setup_action_buttons(main_frame)
        
        # Progress and log section
        self.setup_progress_section(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
    
    def setup_folder_selection(self, parent):
        """Setup folder selection controls"""
        # Folder selection frame
        folder_frame = ttk.LabelFrame(parent, text="Folder Selection", padding="10")
        folder_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(1, weight=1)
        
        # Folder path label
        ttk.Label(folder_frame, text="Target Folder:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Folder path entry
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, width=50)
        self.folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(
            folder_frame, 
            text="Browse...", 
            command=self.browse_folder,
            style='Action.TButton'
        )
        browse_btn.grid(row=0, column=2)
        
        # Drag and drop hint
        self.drop_hint = ttk.Label(
            folder_frame, 
            text="💡 Tip: You can also drag and drop a folder here",
            style='Warning.TLabel'
        )
        self.drop_hint.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        # Check if drag and drop is supported
        try:
            self.root.drop_target_register('DND_Files')
            self.root.dnd_bind('<<Drop>>', self.handle_drop)
            self.drag_drop_supported = True
        except AttributeError:
            # Drag and drop not supported, hide the hint
            self.drop_hint.grid_remove()
            self.drag_drop_supported = False
    
    def setup_options_section(self, parent):
        """Setup organization options"""
        # Options frame
        options_frame = ttk.LabelFrame(parent, text="Organization Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Mode selection
        ttk.Label(options_frame, text="Sorting Mode:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.mode_var = tk.StringVar(value="type")
        mode_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.mode_var,
            values=["type", "size", "date", "content"],
            state="readonly",
            width=15
        )
        mode_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Profile selection
        ttk.Label(options_frame, text="Profile:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.profile_var = tk.StringVar(value="default")
        profile_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.profile_var,
            values=["default", "work", "personal"],
            state="readonly",
            width=15
        )
        profile_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Options row 2
        # Dry run checkbox
        self.dry_run_var = tk.BooleanVar(value=True)
        dry_run_check = ttk.Checkbutton(
            options_frame,
            text="Dry Run (Preview only)",
            variable=self.dry_run_var
        )
        dry_run_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Backup checkbox
        self.backup_var = tk.BooleanVar(value=False)
        backup_check = ttk.Checkbutton(
            options_frame,
            text="Create backup before organizing",
            variable=self.backup_var
        )
        backup_check.grid(row=1, column=2, columnspan=2, sticky=tk.W, pady=(10, 0))
    
    def setup_action_buttons(self, parent):
        """Setup action buttons"""
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        # Organize button
        self.organize_btn = ttk.Button(
            button_frame,
            text="🚀 Organize Files",
            command=self.start_organization,
            style='Primary.TButton'
        )
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(
            button_frame,
            text="⏹️ Stop",
            command=self.stop_organization,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Undo button
        undo_btn = ttk.Button(
            button_frame,
            text="↩️ Undo Last",
            command=self.undo_last_operation
        )
        undo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear log button
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear Log",
            command=self.clear_log
        )
        clear_btn.pack(side=tk.LEFT)
    
    def setup_progress_section(self, parent):
        """Setup progress tracking and log display"""
        # Progress frame
        progress_frame = ttk.LabelFrame(parent, text="Progress & Logs", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="Ready to organize files")
        self.progress_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Log text area
        log_frame = ttk.Frame(progress_frame)
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text widget
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            width=80,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Log scrollbar
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
    
    def setup_status_bar(self, parent):
        """Setup status bar"""
        # Status frame
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # File count label
        self.file_count_var = tk.StringVar(value="Files: 0")
        file_count_label = ttk.Label(status_frame, textvariable=self.file_count_var)
        file_count_label.grid(row=0, column=1, padx=(20, 0))
    
    def setup_bindings(self):
        """Setup event bindings"""
        # Enter key in folder entry
        self.folder_entry.bind('<Return>', lambda e: self.start_organization())
    
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(title="Select folder to organize")
        if folder:
            self.folder_var.set(folder)
            self.selected_folder = folder
            self.update_file_count()
    
    def handle_drop(self, event):
        """Handle drag and drop of folders"""
        files = event.data
        if files:
            # Get the first file/folder path
            path = files[0]
            if os.path.isdir(path):
                self.folder_var.set(path)
                self.selected_folder = path
                self.update_file_count()
                self.log_message(f"📁 Dropped folder: {path}")
            else:
                # If it's a file, get its parent directory
                parent_dir = str(Path(path).parent)
                self.folder_var.set(parent_dir)
                self.selected_folder = parent_dir
                self.update_file_count()
                self.log_message(f"📁 Using parent directory: {parent_dir}")
    
    def update_file_count(self):
        """Update the file count display"""
        if self.selected_folder:
            try:
                folder_path = Path(self.selected_folder)
                file_count = len([f for f in folder_path.iterdir() if f.is_file])
                self.file_count_var.set(f"Files: {file_count}")
            except Exception as e:
                self.file_count_var.set("Files: Error")
    
    def start_organization(self):
        """Start the file organization process"""
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder to organize!")
            return
        
        if not os.path.exists(self.selected_folder):
            messagebox.showerror("Error", "Selected folder does not exist!")
            return
        
        # Disable organize button and enable stop button
        self.organize_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Clear log
        self.clear_log()
        
        # Log start
        self.log_message("🚀 Starting file organization...")
        self.log_message(f"📁 Target: {self.selected_folder}")
        self.log_message(f"🔧 Mode: {self.mode_var.get()}")
        self.log_message(f"👤 Profile: {self.profile_var.get()}")
        self.log_message(f"🔍 Dry Run: {'Yes' if self.dry_run_var.get() else 'No'}")
        self.log_message("-" * 50)
        
        # Start organization in separate thread
        self.organization_thread = threading.Thread(
            target=self.run_organization,
            daemon=True
        )
        self.organization_thread.start()
    
    def run_organization(self):
        """Run the organization process in background thread"""
        try:
            # Update progress
            self.message_queue.put(("progress", 10, "Scanning files..."))
            
            # Run organizer
            results = self.organizer.organize_folder(
                folder_path=self.selected_folder,
                mode=self.mode_var.get(),
                profile=self.profile_var.get(),
                dry_run=self.dry_run_var.get()
            )
            
            # Update progress
            self.message_queue.put(("progress", 100, "Organization completed!"))
            
            # Log results
            if results.get("moved"):
                self.message_queue.put(("log", f"✅ Successfully organized {len(results['moved'])} files"))
                for item in results["moved"]:
                    self.message_queue.put(("log", f"  📄 {item['file']} → {item['category']}"))
            
            if results.get("errors"):
                self.message_queue.put(("log", f"⚠️  {len(results['errors'])} errors occurred"))
                for error in results["errors"]:
                    self.message_queue.put(("log", f"  ❌ {error}"))
            
            # Final status
            if results.get("errors"):
                self.message_queue.put(("status", "Completed with errors"))
            else:
                self.message_queue.put(("status", "Completed successfully"))
                
        except Exception as e:
            self.message_queue.put(("log", f"❌ Error: {str(e)}"))
            self.message_queue.put(("status", "Failed"))
        finally:
            # Re-enable organize button and disable stop button
            self.message_queue.put(("buttons", "enable_organize"))
    
    def stop_organization(self):
        """Stop the current organization process"""
        # This is a placeholder - in a real implementation, you'd need to
        # implement a way to gracefully stop the organizer
        self.log_message("⏹️ Stop requested (not implemented in this version)")
        self.stop_btn.config(state=tk.DISABLED)
    
    def undo_last_operation(self):
        """Undo the last organization operation"""
        try:
            if self.organizer.undo_last_operation():
                self.log_message("↩️ Undo operation completed successfully")
                messagebox.showinfo("Success", "Undo operation completed!")
            else:
                self.log_message("❌ No operations to undo")
                messagebox.showwarning("Warning", "No operations to undo!")
        except Exception as e:
            self.log_message(f"❌ Undo failed: {str(e)}")
            messagebox.showerror("Error", f"Undo operation failed: {str(e)}")
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def log_message(self, message):
        """Add a message to the log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def process_messages(self):
        """Process messages from the background thread"""
        try:
            while True:
                try:
                    msg_type, *args = self.message_queue.get_nowait()
                    
                    if msg_type == "progress":
                        progress, description = args
                        self.progress_var.set(progress)
                        self.progress_label.config(text=description)
                    
                    elif msg_type == "log":
                        message = args[0]
                        self.log_message(message)
                    
                    elif msg_type == "status":
                        status = args[0]
                        self.status_var.set(status)
                    
                    elif msg_type == "buttons":
                        action = args[0]
                        if action == "enable_organize":
                            self.organize_btn.config(state=tk.NORMAL)
                            self.stop_btn.config(state=tk.DISABLED)
                    
                except queue.Empty:
                    break
                    
        except Exception as e:
            print(f"Error processing messages: {e}")
        
        # Schedule next check
        self.root.after(100, self.process_messages)

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = SmartFileOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
