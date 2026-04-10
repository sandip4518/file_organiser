#!/usr/bin/env python3
"""
Smart File Organizer GUI Interface
Provides a modern, premium graphical interface using CustomTkinter
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import threading
import queue
from pathlib import Path
import sys
import os
from PIL import Image

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.file_organizer import FileOrganizer

# Configuration & Appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

COLORS = {
    "bg_main": "#0f111a",
    "bg_sidebar": "#16161e",
    "bg_card": "#1a1b26",
    "accent": "#7aa2f7",
    "success": "#9ece6a",
    "error": "#f7768e",
    "text_main": "#a9b1d6",
    "text_bright": "#cfc9c2",
    "border": "#292e42"
}

import typing

# ... (omitted imports)

class SmartFileOrganizerGUI(ctk.CTk):
    """Main GUI window using CustomTkinter for a Premium Experience"""
    
    def __init__(self):
        super().__init__()
        
        # Window Configuration
        self.title("Smart File Organizer Pro")
        self.geometry("1100x750")
        self.minsize(1000, 680)
        
        # Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize Core
        self.organizer = FileOrganizer()
        self.selected_folder: str = ""
        self.message_queue: queue.Queue = queue.Queue()
        
        # State
        self.total_files: int = 0
        self.organized_files: int = 0
        self.error_count: int = 0
        
        # UI Elements Storage
        self.setup_sidebar()
        self.setup_workspace()
        
        # Start message processing
        self.process_messages()
        
    def setup_sidebar(self):
        """Setup the Sidebar with Branding and Stats"""
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=COLORS["bg_sidebar"])
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Branding
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FileOrganiser", 
                                      font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["text_bright"])
        self.logo_label.grid(row=0, column=0, padx=30, pady=(40, 5), sticky="w")
        
        self.sub_label = ctk.CTkLabel(self.sidebar_frame, text="AI Driven Productivity", 
                                     font=ctk.CTkFont(size=12), text_color=COLORS["text_main"])
        self.sub_label.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="w")
        
        # Stats Section
        self.stats_title = ctk.CTkLabel(self.sidebar_frame, text="DASHBOARD", 
                                       font=ctk.CTkFont(size=11, weight="bold"), text_color=COLORS["accent"])
        self.stats_title.grid(row=2, column=0, padx=30, pady=(10, 15), sticky="w")
        
        # Stats Cards Container
        self.stats_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.stats_container.grid(row=3, column=0, padx=20, sticky="ew")
        self.stats_container.grid_columnconfigure((0, 1), weight=1)
        
        self.stat_widgets = {}
        stats_info = [
            ("Total Files", "0", "📄", 0, 0),
            ("Organized", "0", "✅", 0, 1),
            ("Errors", "0", "❌", 1, 0),
            ("Sessions", "0", "🚀", 1, 1)
        ]
        
        for name, val, icon, r, c in stats_info:
            card = ctk.CTkFrame(self.stats_container, corner_radius=10, fg_color=COLORS["bg_card"], 
                               border_width=1, border_color=COLORS["border"])
            card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            
            ctk.CTkLabel(card, text=f"{icon} {name}", font=ctk.CTkFont(size=10), text_color=COLORS["text_main"]).pack(pady=(10, 0), padx=10, anchor="w")
            val_label = ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=18, weight="bold"), text_color=COLORS["text_bright"])
            val_label.pack(pady=(2, 10), padx=10, anchor="w")
            self.stat_widgets[name] = val_label

        # Bottom Buttons
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=30, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                               command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

    def setup_workspace(self):
        """Setup the Main Interaction Core"""
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLORS["bg_main"])
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(4, weight=1)
        
        # Top Bar (Path Selection)
        self.path_bar = ctk.CTkFrame(self.main_container, corner_radius=12, fg_color=COLORS["bg_card"], 
                                    border_width=1, border_color=COLORS["border"])
        self.path_bar.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        self.path_bar.grid_columnconfigure(0, weight=1)
        
        self.path_label = ctk.CTkLabel(self.path_bar, text="Select a directory to begin...", 
                                      font=ctk.CTkFont(size=13), text_color=COLORS["text_main"], anchor="w")
        self.path_label.grid(row=0, column=0, padx=20, pady=12, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(self.path_bar, text="+ Select Folder", font=ctk.CTkFont(weight="bold"), 
                                       width=140, height=35, fg_color=COLORS["accent"], hover_color="#5a8bed", 
                                       command=self.browse_folder)
        self.browse_btn.grid(row=0, column=1, padx=10, pady=8)
        
        # Hero Action Card (Visual Drop Zone)
        self.hero_card = ctk.CTkFrame(self.main_container, corner_radius=15, fg_color=COLORS["bg_card"],
                                     border_width=1, border_color=COLORS["border"])
        self.hero_card.grid(row=1, column=0, sticky="ew", pady=(0, 30), ipady=20)
        
        self.hero_title = ctk.CTkLabel(self.hero_card, text="Ready to Organize?", 
                                       font=ctk.CTkFont(size=22, weight="bold"), text_color=COLORS["text_bright"])
        self.hero_title.pack(pady=(30, 5))
        
        self.hero_sub = ctk.CTkLabel(self.hero_card, text="Clean up your workspace with smart AI rules in seconds", 
                                     font=ctk.CTkFont(size=13), text_color=COLORS["text_main"])
        self.hero_sub.pack(pady=(0, 25))
        
        self.launch_btn = ctk.CTkButton(self.hero_card, text="START ORGANIZATION", font=ctk.CTkFont(size=14, weight="bold"),
                                        height=45, width=220, fg_color=COLORS["success"], hover_color="#7ab34f",
                                        text_color="#000", command=self.start_organization)
        self.launch_btn.pack(pady=(0, 30))
        
        # Options Toolbar
        self.toolbar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.toolbar.grid(row=2, column=0, sticky="ew", pady=(0, 30))
        
        # Options
        self.mode_label = ctk.CTkLabel(self.toolbar, text="SORTING MODE", font=ctk.CTkFont(size=10, weight="bold"), text_color=COLORS["accent"])
        self.mode_label.grid(row=0, column=0, padx=5, sticky="w")
        self.mode_menu = ctk.CTkOptionMenu(self.toolbar, values=["type", "size", "date", "content"], width=130)
        self.mode_menu.grid(row=1, column=0, padx=5, pady=(5, 0))
        
        self.profile_label = ctk.CTkLabel(self.toolbar, text="PROFILE", font=ctk.CTkFont(size=10, weight="bold"), text_color=COLORS["accent"])
        self.profile_label.grid(row=0, column=1, padx=20, sticky="w")
        self.profile_menu = ctk.CTkOptionMenu(self.toolbar, values=["default", "work", "personal"], width=130)
        self.profile_menu.grid(row=1, column=1, padx=20, pady=(5, 0))
        
        self.dry_run_switch = ctk.CTkSwitch(self.toolbar, text="Dry Run Mode", font=ctk.CTkFont(size=12))
        self.dry_run_switch.grid(row=1, column=2, padx=20)
        self.dry_run_switch.select()
        
        self.undo_btn = ctk.CTkButton(self.toolbar, text="↩ Undo Last", width=120, height=32, 
                                     fg_color=COLORS["error"], hover_color="#d65f6e", command=self.undo_last_operation)
        self.undo_btn.grid(row=1, column=3, padx=(20, 0))
        
        # Log Console
        self.console_frame = ctk.CTkFrame(self.main_container, corner_radius=12, fg_color=COLORS["bg_card"],
                                         border_width=1, border_color=COLORS["border"])
        self.console_frame.grid(row=4, column=0, sticky="nsew")
        self.console_frame.grid_columnconfigure(0, weight=1)
        self.console_frame.grid_rowconfigure(1, weight=1)
        
        self.console_title = ctk.CTkLabel(self.console_frame, text="ACTIVITY LOG", 
                                         font=ctk.CTkFont(size=10, weight="bold"), text_color=COLORS["text_main"])
        self.console_title.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.clear_log_btn = ctk.CTkButton(self.console_frame, text="Clear", width=60, height=22, 
                                          font=ctk.CTkFont(size=10), fg_color=COLORS["border"], hover_color="#3b4261",
                                          command=self.clear_log)
        self.clear_log_btn.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="e")
        
        self.textbox = ctk.CTkTextbox(self.console_frame, font=("Consolas", 12), border_width=0, 
                                     fg_color="transparent", text_color=COLORS["text_main"])
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.main_container, height=6, fg_color=COLORS["bg_card"], progress_color=COLORS["accent"])
        self.progress_bar.grid(row=5, column=0, sticky="ew", pady=(20, 0))
        self.progress_bar.set(0)

    def change_appearance_mode(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select folder to organize")
        if folder:
            self.selected_folder = folder
            self.path_label.configure(text=folder)
            self.log_message(f"📁 Root directory set: {folder}")
            self.update_stats()

    def update_stats(self):
        if self.selected_folder:
            try:
                folder_path = Path(self.selected_folder)
                files = [f for f in folder_path.iterdir() if f.is_file()]
                self.total_files = len(files)
                self.stat_widgets["Total Files"].configure(text=str(self.total_files))
            except Exception:
                self.stat_widgets["Total Files"].configure(text="Err")

    def log_message(self, message):
        self.textbox.insert("end", f"{message}\n")
        self.textbox.see("end")

    def clear_log(self):
        self.textbox.delete("1.0", "end")

    def start_organization(self):
        if not self.selected_folder:
            messagebox.showwarning("No Folder", "Please select a folder first!")
            return
        
        self.launch_btn.configure(state="disabled", text="ORGANIZING...")
        self.clear_log()
        self.log_message("🚀 Analyzing filesystem architecture...")
        
        # Start organization in thread
        threading.Thread(target=self.run_organization, daemon=True).start()

    def run_organization(self):
        try:
            self.message_queue.put(("progress", 0.2))
            
            results = self.organizer.organize_folder(
                folder_path=self.selected_folder,
                mode=self.mode_menu.get(),
                profile=self.profile_menu.get(),
                dry_run=self.dry_run_switch.get()
            )
            
            moved = results.get("moved", [])
            errors = results.get("errors", [])
            
            self.message_queue.put(("log", f"✅ Successfully processed {len(moved)} files"))
            for item in moved:
                self.message_queue.put(("log", f"  • {item['file']} → {item['category']}"))
            
            if errors:
                self.message_queue.put(("log", f"❌ {len(errors)} errors during operation"))
            
            self.message_queue.put(("stats_update", len(moved), len(errors)))
            self.message_queue.put(("progress", 1.0))
            
        except Exception as e:
            self.message_queue.put(("log", f"CRITICAL ERROR: {str(e)}"))
        finally:
            self.message_queue.put(("ui_reset", None))

    def undo_last_operation(self):
        try:
            if self.organizer.undo_last_operation():
                self.log_message("↩ Operation successfully reverted.")
                messagebox.showinfo("Success", "Undo operation completed!")
                self.update_stats()
            else:
                self.log_message("ℹ Nothing to undo.")
        except Exception as e:
            self.log_message(f"❌ Reversion failed: {str(e)}")

    def process_messages(self):
        """Process messages from the background thread with type safety"""
        try:
            while not self.message_queue.empty():
                try:
                    msg = self.message_queue.get_nowait()
                    if not isinstance(msg, (list, tuple)) or len(msg) < 2:
                        continue
                        
                    msg_type = msg[0]
                    
                    if msg_type == "progress":
                        self.progress_bar.set(float(msg[1]))
                    elif msg_type == "log":
                        self.log_message(str(msg[1]))
                    elif msg_type == "stats_update":
                        if len(msg) >= 3:
                            moved = int(msg[1])
                            errors = int(msg[2])
                            self.organized_files += moved
                            self.error_count += errors
                            if "Organized" in self.stat_widgets:
                                self.stat_widgets["Organized"].configure(text=str(self.organized_files))
                            if "Errors" in self.stat_widgets:
                                self.stat_widgets["Errors"].configure(text=str(self.error_count))
                    elif msg_type == "ui_reset":
                        self.launch_btn.configure(state="normal", text="START ORGANIZATION")
                        self.update_stats()
                except (queue.Empty, IndexError, ValueError):
                    break
        except Exception:
            pass
        self.after(100, self.process_messages)

if __name__ == "__main__":
    app = SmartFileOrganizerGUI()
    app.mainloop()
