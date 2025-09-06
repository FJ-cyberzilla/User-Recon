# user_recon/ui/banner.py

import os
import platform
import psutil
import time
import sys
from rich.console import Console
from rich.text import Text

console = Console()


def beep():
    """Cross-platform one-time beep."""
    try:
        if sys.platform == "win32":
            import winsound
            winsound.Beep(1000, 200)
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()
    except Exception:
        pass


def typing_effect(text: str, delay: float = 0.02, style: str = "bold green"):
    """Print text with typing animation."""
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(delay)
    console.print("")  # new line


def get_system_info():
    """Gather system information for the banner."""
    info = {
        "OS": platform.system() + " " + platform.release(),
        "Python": platform.python_version(),
        "CPU": platform.processor(),
        "Cores": str(psutil.cpu_count(logical=True)),
        "RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
    }
    return info


def show_banner():
    """Display the main banner with system info and animation."""
    banner = Text(
        r"""
M""MMMMM""M                               MM"""""""`MM
M  MMMMM  M                               MM  mmmm,  M
M  MMMMM  M .d8888b. .d8888b. 88d888b.    M'        .M .d8888b. .d8888b. .d8888b. 88d888b.
M  MMMMM  M Y8ooooo. 88ooood8 88'  `88    MM  MMMb. "M 88ooood8 88'  `"" 88'  `88 88'  `88
M  `MMM'  M       88 88.  ... 88          MM  MMMMM  M 88.  ... 88.  ... 88.  .88 88    88
Mb       dM `88888P' `88888P' dP          MM  MMMMM  M `88888P' `88888P' `88888P' dP    dP
MMMMMMMMMMM                               MMMMMMMMMMMM
        """,
        style="bold green",
    )

    console.print(banner)

    # Typing effect
    typing_effect(">>> User Recon - Advanced OSINT & AI Analysis <<<", style="bold yellow")

    # System info
    sysinfo = get_system_info()
    console.print("\n[bold blue]System Information:[/bold blue]")
    for k, v in sysinfo.items():
        console.print(f" [green]{k}[/green]: {v}")

    console.print("\n[cyan]Initialization complete. Ready to scan.[/cyan]")

    # One-time beep
    beep()


if __name__ == "__main__":
    show_banner()
