
import os
import shutil
import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

console = Console()

class FileOrganizer:
    """
    Advanced File Organizer with smart categorization, rules engine, and multiple sorting modes
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.operation_history = []
        self.duplicate_hashes = {}
        
    def _load_config(self) -> dict:
        """Load configuration from YAML file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                # Load default config
                default_config_path = "config/default_config.yaml"
                if os.path.exists(default_config_path):
                    with open(default_config_path, 'r', encoding='utf-8') as f:
                        return yaml.safe_load(f)
                else:
                    console.print("[red]No configuration file found![/red]")
                    return {}
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            return {}
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('FileOrganizer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('organizer.log', encoding='utf-8')
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def organize_folder(self, folder_path: str, mode: str = "type", 
                       profile: str = "default", dry_run: bool = False) -> Dict:
        """
        Organize files in the specified folder based on mode and profile
        
        Args:
            folder_path: Path to organize
            mode: Sorting mode (type, size, date, content)
            profile: Configuration profile to use
            dry_run: Show plan without moving files
            
        Returns:
            Dictionary with organization results
        """
        folder_path = Path(folder_path)
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder {folder_path} does not exist")
        
        self.logger.info(f"Starting organization of {folder_path} with mode: {mode}, profile: {profile}")
        
        # Get profile configuration
        profile_config = self.config.get('profiles', {}).get(profile, {})
        enabled_categories = profile_config.get('enabled_categories', [])
        
        # Scan files
        files = self._scan_files(folder_path)
        
        # Apply organization based on mode
        if mode == "type":
            plan = self._organize_by_type(files, folder_path, enabled_categories)
        elif mode == "size":
            plan = self._organize_by_size(files, folder_path)
        elif mode == "date":
            plan = self._organize_by_date(files, folder_path)
        elif mode == "content":
            plan = self._organize_by_content(files, folder_path)
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        # Apply custom rules
        plan = self._apply_custom_rules(plan, profile_config.get('rules', []))
        
        # Handle duplicates
        plan = self._handle_duplicates(plan)
        
        # Execute plan if not dry run
        results = {"moved": [], "errors": [], "duplicates": []}
        
        if not dry_run:
            results = self._execute_plan(plan, folder_path)
            self._log_operation(folder_path, mode, profile, results)
        else:
            console.print("[yellow]DRY RUN MODE - No files will be moved[/yellow]")
            self._display_plan(plan)
        
        return results
    
    def _scan_files(self, folder_path: Path) -> List[Path]:
        """Scan folder for files, excluding system files and folders"""
        files = []
        for item in folder_path.iterdir():
            if item.is_file():
                # Skip hidden files and system files
                if not item.name.startswith('.') and not item.name.startswith('~'):
                    files.append(item)
        return files
    
    def _organize_by_type(self, files: List[Path], base_path: Path, 
                          enabled_categories: List[str]) -> List[Dict]:
        """Organize files by their type/extension"""
        plan = []
        
        for file in files:
            file_ext = file.suffix.lower().lstrip('.')
            
            # Find matching category
            target_category = None
            for category_name, category_config in self.config.get('categories', {}).items():
                if category_name in enabled_categories:
                    if file_ext in category_config.get('extensions', []):
                        target_category = category_config['folder_name']
                        break
            
            if target_category:
                plan.append({
                    'file': file,
                    'action': 'move',
                    'source': str(file),
                    'target': str(base_path / target_category / file.name),
                    'category': target_category,
                    'reason': f'File type: {file_ext}'
                })
            else:
                plan.append({
                    'file': file,
                    'action': 'move',
                    'source': str(file),
                    'target': str(base_path / 'Others' / file.name),
                    'category': 'Others',
                    'reason': 'Uncategorized file type'
                })
        
        return plan
    
    def _organize_by_size(self, files: List[Path], base_path: Path) -> List[Dict]:
        """Organize files by size"""
        plan = []
        size_categories = self.config.get('size_categories', {})
        
        for file in files:
            file_size = file.stat().st_size
            
            # Determine size category
            target_category = 'Others'
            for category, max_size in size_categories.items():
                if file_size <= max_size:
                    target_category = category
                    break
            
            plan.append({
                'file': file,
                'action': 'move',
                'source': str(file),
                'target': str(base_path / target_category / file.name),
                'category': target_category,
                'reason': f'Size: {self._format_size(file_size)}'
            })
        
        return plan
    
    def _organize_by_date(self, files: List[Path], base_path: Path) -> List[Dict]:
        """Organize files by modification date"""
        plan = []
        date_categories = self.config.get('date_categories', {})
        now = datetime.now()
        
        for file in files:
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            days_ago = (now - mtime).days
            
            # Determine date category
            target_category = 'Old_Files'
            for category, max_days in date_categories.items():
                if days_ago <= max_days:
                    target_category = category
                    break
            
            plan.append({
                'file': file,
                'action': 'move',
                'source': str(file),
                'target': str(base_path / target_category / file.name),
                'category': target_category,
                'reason': f'Modified: {days_ago} days ago'
            })
        
        return plan
    
    def _organize_by_content(self, files: List[Path], base_path: Path) -> List[Dict]:
        """Organize files by content analysis (basic keyword detection)"""
        plan = []
        
        for file in files:
            target_category = 'Others'
            reason = 'Content analysis'
            
            # Basic content detection for text files
            if file.suffix.lower() in ['.txt', '.md', '.py', '.js', '.html', '.css']:
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1024).lower()  # Read first 1KB
                        
                        if any(keyword in content for keyword in ['invoice', 'bill', 'receipt']):
                            target_category = 'Invoices'
                            reason = 'Contains invoice-related content'
                        elif any(keyword in content for keyword in ['resume', 'cv', 'curriculum']):
                            target_category = 'Resumes'
                            reason = 'Contains resume-related content'
                        elif any(keyword in content for keyword in ['password', 'secret', 'key']):
                            target_category = 'Sensitive'
                            reason = 'Contains sensitive content'
                except:
                    pass
            
            plan.append({
                'file': file,
                'action': 'move',
                'source': str(file),
                'target': str(base_path / target_category / file.name),
                'category': target_category,
                'reason': reason
            })
        
        return plan
    
    def _apply_custom_rules(self, plan: List[Dict], enabled_rules: List[str]) -> List[Dict]:
        """Apply custom rules to the organization plan"""
        rules = self.config.get('rules', [])
        
        for rule in rules:
            if rule['name'] in enabled_rules:
                for item in plan:
                    if self._evaluate_rule_condition(item, rule['condition']):
                        item['target'] = str(Path(item['target']).parent / rule['target'] / Path(item['target']).name)
                        item['category'] = rule['target']
                        item['reason'] = f"Custom rule: {rule['name']}"
        
        return plan
    
    def _evaluate_rule_condition(self, item: Dict, condition: str) -> bool:
        """Evaluate a rule condition for a file item"""
        try:
            file = item['file']
            file_ext = file.suffix.lower().lstrip('.')
            file_size = file.stat().st_size
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            days_ago = (datetime.now() - mtime).days
            
            # Simple condition evaluation (in production, use a proper expression parser)
            if 'extension ==' in condition and f"'{file_ext}'" in condition:
                if 'size >' in condition:
                    size_limit = int(condition.split('size >')[1].split()[0])
                    return file_size > size_limit
                return True
            elif 'filename_contains' in condition:
                keywords = [kw.strip("'") for kw in condition.split('filename_contains(')[1:]]
                keywords = [kw.split(')')[0] for kw in keywords]
                return any(keyword.lower() in file.name.lower() for keyword in keywords)
            elif 'modified_days_ago >' in condition:
                days_limit = int(condition.split('>')[1].strip())
                return days_ago > days_limit
            
            return False
        except:
            return False
    
    def _handle_duplicates(self, plan: List[Dict]) -> List[Dict]:
        """Handle duplicate files by renaming them"""
        seen_names = {}
        
        for item in plan:
            target_path = Path(item['target'])
            original_name = target_path.name
            
            if original_name in seen_names:
                # Generate unique name
                name, ext = os.path.splitext(original_name)
                counter = seen_names[original_name] + 1
                new_name = f"{name}({counter}){ext}"
                
                while new_name in seen_names:
                    counter += 1
                    new_name = f"{name}({counter}){ext}"
                
                item['target'] = str(target_path.parent / new_name)
                seen_names[original_name] = counter
            else:
                seen_names[original_name] = 1
        
        return plan
    
    def _execute_plan(self, plan: List[Dict], base_path: Path) -> Dict:
        """Execute the organization plan"""
        results = {"moved": [], "errors": [], "duplicates": []}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Organizing files...", total=len(plan))
            
            for item in plan:
                try:
                    # Create target directory
                    target_path = Path(item['target'])
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    shutil.move(item['source'], item['target'])
                    
                    results["moved"].append({
                        'file': item['file'].name,
                        'from': item['source'],
                        'to': item['target'],
                        'category': item['category'],
                        'reason': item['reason']
                    })
                    
                    self.logger.info(f"Moved {item['file'].name} to {item['category']}")
                    
                except Exception as e:
                    error_msg = f"Error moving {item['file'].name}: {str(e)}"
                    results["errors"].append(error_msg)
                    self.logger.error(error_msg)
                
                progress.advance(task)
        
        return results
    
    def _display_plan(self, plan: List[Dict]):
        """Display the organization plan"""
        table = Table(title="Organization Plan")
        table.add_column("File", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Reason", style="yellow")
        
        for item in plan:
            table.add_row(
                Path(item['source']).name,
                item['category'],
                item['reason']
            )
        
        console.print(table)
    
    def _log_operation(self, folder_path: Path, mode: str, profile: str, results: Dict):
        """Log the operation for undo functionality"""
        operation = {
            'timestamp': datetime.now().isoformat(),
            'folder': str(folder_path),
            'mode': mode,
            'profile': profile,
            'moved_files': results.get('moved', []),
            'errors': results.get('errors', [])
        }
        
        self.operation_history.append(operation)
        
        # Save to file
        with open('operation_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.operation_history, f, indent=2, ensure_ascii=False)
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def undo_last_operation(self) -> bool:
        """Undo the last organization operation"""
        if not self.operation_history:
            console.print("[red]No operations to undo[/red]")
            return False
        
        last_op = self.operation_history.pop()
        console.print(f"[yellow]Undoing operation from {last_op['timestamp']}[/yellow]")
        
        # Implementation for undo would go here
        # This is a placeholder for the undo functionality
        
        return True
