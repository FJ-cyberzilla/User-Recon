# user_recon/ui/reports.py

import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED

console = Console()


class ReportUI:
    """
    Render sleek, modern reports for User Recon.
    Combines AI analysis, pattern recognition, entropy, anomaly, and predictions.
    """

    @staticmethod
    def show_report(report: dict):
        username = report.get("username", "N/A")
        analysis = report.get("analysis", {})

        console.print(Panel.fit(
            f"[bold cyan]User Recon Intelligence Report[/bold cyan]\n"
            f"[yellow]Subject:[/yellow] {username}\n"
            f"[green]Timestamp:[/green] {report.get('timestamp', 'N/A')}",
            style="bold green",
            box=ROUNDED
        ))

        # --- Social Media Presence ---
        social = analysis.get("social_presence", {})
        if social:
            table = Table(title="🌍 Social Media Presence", box=ROUNDED, style="cyan")
            table.add_column("Platform", style="bold yellow")
            table.add_column("Status", style="bold green")
            for platform, status in social.items():
                table.add_row(platform, str(status))
            console.print(table)

        # --- Entropy Analysis ---
        entropy = analysis.get("entropy", {})
        if entropy:
            console.print(Panel.fit(
                f"🔑 [bold cyan]Entropy Analysis[/bold cyan]\n"
                f" Raw: {entropy.get('raw', 0)}\n"
                f" Normalized: {entropy.get('normalized', 0)}\n"
                f" Class: {entropy.get('class', 'N/A')}",
                style="bold magenta",
                box=ROUNDED
            ))

        # --- Predictive Aliases ---
        predictions = analysis.get("predicted_aliases", [])
        if predictions:
            table = Table(title="🔮 Predictive Aliases", box=ROUNDED, style="yellow")
            table.add_column("Candidate", style="cyan")
            table.add_column("Similarity %", justify="center")
            table.add_column("Entropy Δ", justify="center")
            table.add_column("Likelihood %", justify="center")
            for p in predictions:
                table.add_row(
                    p["candidate"],
                    str(p["similarity"]),
                    str(p["entropy_diff"]),
                    str(p["likelihood_score"])
                )
            console.print(table)

        # --- Anomaly Reports ---
        anomalies = analysis.get("anomaly_reports", [])
        if anomalies:
            console.print(Panel.fit(
                "🚨 [bold red]Anomaly Detection[/bold red]\n" +
                "\n".join([f"- {a}" for a in anomalies]),
                style="red",
                box=ROUNDED
            ))

        console.print("\n[green bold]✔ Report generation complete[/green bold]")

    @staticmethod
    def save_report(report: dict, path: str):
        """Save JSON report to file."""
        with open(path, "w") as f:
            json.dump(report, f, indent=4)
        console.print(f"[cyan]Report saved to[/cyan] [bold green]{path}[/bold green]")


if __name__ == "__main__":
    # Demo run
    sample = {
        "username": "elhamjvdi",
        "timestamp": "2025-09-06T12:00:00Z",
        "analysis": {
            "social_presence": {"Twitter": "FOUND", "Facebook": "NOT FOUND"},
            "entropy": {"raw": 3.21, "normalized": 0.68, "class": "Medium"},
            "predicted_aliases": [
                {"candidate": "elhamjvdi2024", "similarity": 92.3, "entropy_diff": 0.12, "likelihood_score": 91.0},
                {"candidate": "_elhamjvdi_", "similarity": 88.7, "entropy_diff": 0.05, "likelihood_score": 89.0}
            ],
            "anomaly_reports": [
                "Username 'X9f!@kPz' flagged as anomaly. Entropy=4.1, Length=8, SpecialChars=0.5. Pattern deviates significantly.",
                "Username 'elham2023' considered normal. Entropy=3.0, Length=9, SpecialChars=0.0. Fits expected distribution."
            ]
        }
    }

    ReportUI.show_report(sample)
