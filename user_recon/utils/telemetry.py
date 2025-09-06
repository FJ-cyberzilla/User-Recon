# user_recon/util/telemetry.py

import os
import json
import time
import socket
import platform
import threading
from datetime import datetime
from user_recon.util.helpers import Helpers


class Telemetry:
    """
    Lightweight telemetry collector for User Recon.
    Tracks execution metrics, system info, and usage patterns.
    """

    def __init__(self, enable: bool = True, file_path: str = "results/telemetry.jsonl"):
        self.enable = enable
        self.file_path = file_path
        self.start_time = time.time()
        self.lock = threading.Lock()

        if self.enable:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # -------------------------------
    # Core collection
    # -------------------------------
    def log_event(self, event_type: str, data: dict = None):
        """Log a structured event to file."""
        if not self.enable:
            return

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "data": data or {},
        }

        with self.lock:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")

    def log_metric(self, metric_name: str, value: float):
        """Log a numeric metric."""
        self.log_event("metric", {"name": metric_name, "value": value})

    def log_username_scan(self, username: str, sites_checked: int, found: int):
        """Specialized telemetry event for username scans."""
        self.log_event(
            "username_scan",
            {
                "username": username,
                "sites_checked": sites_checked,
                "sites_found": found,
            },
        )

    def session_summary(self):
        """Summarize current session performance."""
        runtime = round(time.time() - self.start_time, 2)
        sysinfo = Helpers.system_info()

        summary = {
            "runtime_seconds": runtime,
            "system_info": sysinfo,
            "timestamp": Helpers.timestamp(),
        }

        self.log_event("session_summary", summary)
        return summary


if __name__ == "__main__":
    telemetry = Telemetry(enable=True)

    telemetry.log_event("app_start", {"version": "2.0"})
    telemetry.log_metric("cpu_usage", 12.3)
    telemetry.log_username_scan("elhamjvdi", sites_checked=20, found=5)

    print("Telemetry summary:", telemetry.session_summary())
