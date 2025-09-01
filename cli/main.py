#!/usr/bin/env python3
"""
Smart File Organizer CLI Interface
Provides a command-line interface for the advanced file organizer
"""

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core.file_organizer import FileOrganizer

console = Console()

def print_banner():
    """Print the application banner"""
    banner = """
    [bold blue]╔══════════════════════════════════════════════════════════════╗[/bold blue]
    [bold blue]║                    SMART FILE ORGANIZER                     ║[/bold blue]
    [bold blue]║                 Advanced Productivity Tool                   ║[/bold blue]
    [bold blue]╚══════════════════════════════════════════════════════════════╝[/bold blue]
    """
    console.print(Panel(banner, style="bold cyan"))

def print_help():
    """Print detailed help information"""
    help_text = """
    [bold]Available Modes:[/bold]
    • [green]type[/green] - Organize by file type/extension (default)
    • [green]size[/green] - Organize by file size (Tiny, Medium, Large, Huge)
    • [green]date[/green] - Organize by modification date
    • [green]content[/green] - Organize by file content analysis
    
    [bold]Available Profiles:[/bold]
    • [green]default[/green] - All categories and rules enabled
    • [green]work[/green] - Work-focused (Documents, Code, Archives)
    • [green]personal[/green] - Personal files (Images, Audio, Video)
    
    [bold]Examples:[/bold]
    • Organize Downloads folder: [cyan]python main.py --path "C:\\Users\\Username\\Downloads"[/cyan]
    • Dry run to see plan: [cyan]python main.py --path "C:\\Users\\Username\\Downloads" --dry-run[/cyan]
    • Organize by size: [cyan]python main.py --path "C:\\Users\\Username\\Downloads" --mode size[/cyan]
    • Use work profile: [cyan]python main.py --path "C:\\Users\\Username\\Downloads" --profile work[/cyan]
    • Undo last operation: [cyan]python main.py --undo[/cyan]
    """
    
    console.print(Panel(help_text, title="[bold]Help & Examples[/bold]", style="bold yellow"))

def validate_path(path: str) -> Path:
    """Validate and return the folder path"""
    folder_path = Path(path)
    if not folder_path.exists():
        console.print(f"[red]Error: Folder '{path}' does not exist![/red]")
        sys.exit(1)
    if not folder_path.is_dir():
        console.print(f"[red]Error: '{path}' is not a directory![/red]")
        sys.exit(1)
    return folder_path

def display_results(results: dict, dry_run: bool = False):
    """Display organization results"""
    if dry_run:
        console.print("\n[bold green]✅ Dry run completed successfully![/bold green]")
        return
    
    # Display moved files
    if results.get("moved"):
        table = Table(title="[bold green]Files Organized Successfully[/bold green]")
        table.add_column("File", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Reason", style="yellow")
        
        for item in results["moved"]:
            table.add_row(
                item['file'],
                item['category'],
                item['reason']
            )
        
        console.print(table)
    
    # Display errors
    if results.get("errors"):
        console.print("\n[bold red]⚠️  Errors occurred:[/bold red]")
        for error in results["errors"]:
            console.print(f"[red]• {error}[/red]")
    
    # Summary
    moved_count = len(results.get("moved", []))
    error_count = len(results.get("errors", []))
    
    if error_count == 0:
        console.print(f"\n[bold green]✅ Successfully organized {moved_count} files![/bold green]")
    else:
        console.print(f"\n[bold yellow]⚠️  Organized {moved_count} files with {error_count} errors[/bold yellow]")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Smart File Organizer - Advanced productivity tool for organizing files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --path "C:\\Users\\Username\\Downloads"
  %(prog)s --path "C:\\Users\\Username\\Downloads" --dry-run
  %(prog)s --path "C:\\Users\\Username\\Downloads" --mode size --profile work
  %(prog)s --undo
        """
    )
    
    parser.add_argument(
        "--path", "-p",
        type=str,
        help="Path to the folder to organize"
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
        "--undo", "-u",
        action="store_true",
        help="Undo the last organization operation"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to custom configuration file"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Handle help
    if len(sys.argv) == 1:
        print_help()
        return
    
    # Handle undo
    if args.undo:
        try:
            organizer = FileOrganizer(args.config) if args.config else FileOrganizer()
            if organizer.undo_last_operation():
                console.print("[bold green]✅ Undo operation completed![/bold green]")
            else:
                console.print("[bold red]❌ Undo operation failed![/bold red]")
        except Exception as e:
            console.print(f"[bold red]❌ Error during undo: {e}[/bold red]")
        return
    
    # Validate path
    if not args.path:
        console.print("[red]Error: --path argument is required![/red]")
        console.print("Use --help for more information.")
        sys.exit(1)
    
    folder_path = validate_path(args.path)
    
    # Initialize organizer
    try:
        config_path = args.config if args.config else None
        organizer = FileOrganizer(config_path) if config_path else FileOrganizer()
        
        console.print(f"[bold]Organizing folder:[/bold] [cyan]{folder_path}[/cyan]")
        console.print(f"[bold]Mode:[/bold] [green]{args.mode}[/green]")
        console.print(f"[bold]Profile:[/bold] [green]{args.profile}[/green]")
        console.print(f"[bold]Dry run:[/bold] [yellow]{'Yes' if args.dry_run else 'No'}[/yellow]")
        
        if args.verbose:
            console.print(f"[bold]Config file:[/bold] [cyan]{organizer.config_path}[/cyan]")
        
        console.print("\n" + "="*60 + "\n")
        
        # Organize folder
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Initializing...", total=None)
            
            try:
                results = organizer.organize_folder(
                    folder_path=str(folder_path),
                    mode=args.mode,
                    profile=args.profile,
                    dry_run=args.dry_run
                )
                
                progress.update(task, description="✅ Organization completed!")
                
            except Exception as e:
                progress.update(task, description="❌ Organization failed!")
                console.print(f"\n[bold red]Error: {e}[/bold red]")
                sys.exit(1)
        
        # Display results
        display_results(results, args.dry_run)
        
        # Additional information
        if not args.dry_run:
            console.print(f"\n[dim]Log file: organizer.log[/dim]")
            console.print(f"[dim]Operation history: operation_history.json[/dim]")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Fatal error: {e}[/bold red]")
        if args.verbose:
            import traceback
            console.print(f"\n[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        sys.exit(1)
