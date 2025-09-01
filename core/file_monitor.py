#!/usr/bin/env python3
"""
File Monitor for Smart File Organizer
Provides real-time monitoring and auto-organization of new files
"""

import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from typing import Optional, Callable
from rich.console import Console

console = Console()

class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system events"""
    
    def __init__(self, organizer, config: dict):
        self.organizer = organizer
        self.config = config
        self.logger = logging.getLogger('FileMonitor')
        self.pending_files = set()
        self.processing_lock = threading.Lock()
        
    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            self._schedule_organization(event.src_path)
    
    def on_moved(self, event):
        """Handle file move events"""
        if not event.is_directory:
            self._schedule_organization(event.dest_path)
    
    def _schedule_organization(self, file_path: str):
        """Schedule a file for organization"""
        with self.processing_lock:
            self.pending_files.add(file_path)
        
        # Start organization thread if not already running
        if not hasattr(self, 'organization_thread') or not self.organization_thread.is_alive():
            self.organization_thread = threading.Thread(target=self._process_pending_files, daemon=True)
            self.organization_thread.start()
    
    def _process_pending_files(self):
        """Process all pending files for organization"""
        while True:
            time.sleep(2)  # Wait for file operations to complete
            
            with self.processing_lock:
                if not self.pending_files:
                    break
                
                files_to_process = list(self.pending_files)
                self.pending_files.clear()
            
            # Process each file
            for file_path in files_to_process:
                try:
                    self._organize_single_file(file_path)
                except Exception as e:
                    self.logger.error(f"Error organizing {file_path}: {e}")
    
    def _organize_single_file(self, file_path: str):
        """Organize a single file"""
        try:
            file_path_obj = Path(file_path)
            
            # Wait for file to be fully written
            if not file_path_obj.exists():
                return
            
            # Check if file is still being written
            initial_size = file_path_obj.stat().st_size
            time.sleep(1)
            current_size = file_path_obj.stat().st_size
            
            if initial_size != current_size:
                # File is still being written, skip for now
                return
            
            # Organize the file
            self.logger.info(f"Auto-organizing: {file_path}")
            
            # Use the organizer to organize the parent directory
            parent_dir = str(file_path_obj.parent)
            self.organizer.organize_folder(
                folder_path=parent_dir,
                mode=self.config.get('auto_mode', 'type'),
                profile=self.config.get('auto_profile', 'default'),
                dry_run=False
            )
            
        except Exception as e:
            self.logger.error(f"Error in auto-organization of {file_path}: {e}")

class FileMonitor:
    """File monitoring system for auto-organization"""
    
    def __init__(self, organizer, config: dict):
        self.organizer = organizer
        self.config = config
        self.observer = Observer()
        self.handler = FileChangeHandler(organizer, config)
        self.monitored_paths = set()
        self.is_running = False
        self.logger = logging.getLogger('FileMonitor')
        
    def add_watch(self, path: str, recursive: bool = True):
        """Add a path to monitor"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                self.logger.error(f"Path does not exist: {path}")
                return False
            
            if not path_obj.is_dir():
                self.logger.error(f"Path is not a directory: {path}")
                return False
            
            # Add to observer
            self.observer.schedule(self.handler, str(path_obj), recursive=recursive)
            self.monitored_paths.add(str(path_obj))
            
            self.logger.info(f"Added watch for: {path} (recursive: {recursive})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding watch for {path}: {e}")
            return False
    
    def remove_watch(self, path: str):
        """Remove a monitored path"""
        try:
            # Find and remove the watch
            for watch in self.observer.emitters:
                if watch.watch.path == path:
                    self.observer.unschedule(watch)
                    self.monitored_paths.discard(path)
                    self.logger.info(f"Removed watch for: {path}")
                    return True
            
            self.logger.warning(f"Watch not found for: {path}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error removing watch for {path}: {e}")
            return False
    
    def start_monitoring(self):
        """Start the file monitoring"""
        if self.is_running:
            self.logger.warning("File monitoring is already running")
            return
        
        if not self.monitored_paths:
            self.logger.error("No paths to monitor. Add paths first.")
            return
        
        try:
            self.observer.start()
            self.is_running = True
            self.logger.info("File monitoring started")
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
        except Exception as e:
            self.logger.error(f"Error starting file monitoring: {e}")
            self.is_running = False
    
    def stop_monitoring(self):
        """Stop the file monitoring"""
        if not self.is_running:
            return
        
        try:
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            self.logger.info("File monitoring stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping file monitoring: {e}")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        try:
            while self.is_running:
                time.sleep(1)
                
                # Check if observer is still running
                if not self.observer.is_alive():
                    self.logger.error("Observer thread died, restarting...")
                    self.observer.start()
                
        except Exception as e:
            self.logger.error(f"Error in monitor loop: {e}")
            self.is_running = False
    
    def get_status(self) -> dict:
        """Get current monitoring status"""
        return {
            'is_running': self.is_running,
            'monitored_paths': list(self.monitored_paths),
            'observer_alive': self.observer.is_alive() if hasattr(self.observer, 'is_alive') else False
        }
    
    def list_watches(self) -> list:
        """List all active watches"""
        watches = []
        for watch in self.observer.emitters:
            watches.append({
                'path': watch.watch.path,
                'recursive': watch.watch.is_recursive
            })
        return watches

class ScheduledOrganizer:
    """Scheduled file organization"""
    
    def __init__(self, organizer, config: dict):
        self.organizer = organizer
        self.config = config
        self.scheduler_thread = None
        self.is_running = False
        self.logger = logging.getLogger('ScheduledOrganizer')
        
    def start_scheduler(self):
        """Start the scheduled organization"""
        if self.is_running:
            self.logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Scheduled organization started")
    
    def stop_scheduler(self):
        """Stop the scheduled organization"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        self.logger.info("Scheduled organization stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                # Get schedule configuration
                schedule_config = self.config.get('schedule', {})
                
                # Check daily schedule
                if schedule_config.get('daily', False):
                    self._check_daily_schedule()
                
                # Check weekly schedule
                if schedule_config.get('weekly', False):
                    self._check_weekly_schedule()
                
                # Check monthly schedule
                if schedule_config.get('monthly', False):
                    self._check_monthly_schedule()
                
                # Sleep for 1 hour before next check
                time.sleep(3600)
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(3600)  # Continue after error
    
    def _check_daily_schedule(self):
        """Check if daily organization should run"""
        schedule_config = self.config.get('schedule', {})
        daily_time = schedule_config.get('daily_time', '02:00')
        
        current_time = time.strftime('%H:%M')
        if current_time == daily_time:
            self._run_scheduled_organization('daily')
    
    def _check_weekly_schedule(self):
        """Check if weekly organization should run"""
        schedule_config = self.config.get('schedule', {})
        weekly_day = schedule_config.get('weekly_day', 'sunday')
        weekly_time = schedule_config.get('weekly_time', '03:00')
        
        current_day = time.strftime('%A').lower()
        current_time = time.strftime('%H:%M')
        
        if current_day == weekly_day and current_time == weekly_time:
            self._run_scheduled_organization('weekly')
    
    def _check_monthly_schedule(self):
        """Check if monthly organization should run"""
        schedule_config = self.config.get('schedule', {})
        monthly_day = schedule_config.get('monthly_day', 1)
        monthly_time = schedule_config.get('monthly_time', '04:00')
        
        current_day = int(time.strftime('%d'))
        current_time = time.strftime('%H:%M')
        
        if current_day == monthly_day and current_time == monthly_time:
            self._run_scheduled_organization('monthly')
    
    def _run_scheduled_organization(self, schedule_type: str):
        """Run scheduled organization"""
        try:
            self.logger.info(f"Running {schedule_type} scheduled organization")
            
            # Get paths to organize
            paths_to_organize = self.config.get('scheduled_paths', [])
            
            for path in paths_to_organize:
                try:
                    self.organizer.organize_folder(
                        folder_path=path,
                        mode=self.config.get('scheduled_mode', 'type'),
                        profile=self.config.get('scheduled_profile', 'default'),
                        dry_run=False
                    )
                    self.logger.info(f"Completed scheduled organization of: {path}")
                    
                except Exception as e:
                    self.logger.error(f"Error in scheduled organization of {path}: {e}")
            
        except Exception as e:
            self.logger.error(f"Error running scheduled organization: {e}")
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            'is_running': self.is_running,
            'schedule_config': self.config.get('schedule', {}),
            'scheduled_paths': self.config.get('scheduled_paths', [])
        }
