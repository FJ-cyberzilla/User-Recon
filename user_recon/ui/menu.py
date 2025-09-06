# user_recon/ui/menu.py

import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()


def typing_effect(text: str, delay: float = 0.03):
    """Simulate typing animation for menu banner."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_banner():
    """Display green vintage cyber banner with animal theme."""
    banner = r"""
       ███    ███ ██    ██ ███████ ██████      ██████  ███████  ██████  ██████   ██████  ███    ██
       ████  ████ ██    ██ ██      ██   ██     ██   ██ ██      ██    ██ ██   ██ ██    ██ ████   ██
       ██ ████ ██ ██    ██ █████   ██████      ██████  █████   ██    ██ ██████  ██    ██ ██ ██  ██
       ██  ██  ██ ██    ██ ██      ██   ██     ██   ██ ██      ██    ██ ██   ██ ██    ██ ██  ██ ██
       ██      ██  ██████  ███████ ██   ██     ██   ██ ███████  ██████  ██   ██  ██████  ██   ████
    """
    console.print(Panel(banner, title="[bold green]User Recon[/bold green]", subtitle="[yellow]AI OSINT Intelligence[/yellow]", style="cyan"))


def main_menu() -> str:
    """Render modern menu with colorful choices."""
    show_banner()

    typing_effect("Welcome, Operator. Choose your path:", delay=0.02)

    menu_items = {
        "1": "🦊 [bold green]Start Recon[/bold green] - Launch username analysis",
        "2": "🦉 [yellow]Reports[/yellow] - View saved intelligence files",
        "3": "🐍 [cyan]Settings[/cyan] - Configure modules & AI parameters",
        "4": "🐺 [red]Exit[/red] - Leave the system"
    }

    for key, value in menu_items.items():
        console.print(f" {key}. {value}")

    choice = Prompt.ask("\n[bold green]Select an option[/bold green]", choices=list(menu_items.keys()))
    return choice


if __name__ == "__main__":
    opt = main_menu()
    console.print(f"You selected: {opt}", style="bold magenta")
