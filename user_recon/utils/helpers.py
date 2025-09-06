# user_recon/util/helpers.py

import socket
import platform
import psutil
import datetime
import hashlib
import random
import string


class Helpers:
    """
    General-purpose helper utilities for User Recon.
    """

    # -------------------------------
    # System Information
    # -------------------------------
    @staticmethod
    def system_info() -> dict:
        """Return basic system information."""
        return {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "cpu_count": psutil.cpu_count(logical=True),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        }

    # -------------------------------
    # Time utilities
    # -------------------------------
    @staticmethod
    def timestamp() -> str:
        """Return current timestamp (ISO format)."""
        return datetime.datetime.utcnow().isoformat()

    @staticmethod
    def pretty_time() -> str:
        """Return human-readable current time."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -------------------------------
    # Hashing utilities
    # -------------------------------
    @staticmethod
    def md5_hash(value: str) -> str:
        return hashlib.md5(value.encode("utf-8")).hexdigest()

    @staticmethod
    def sha1_hash(value: str) -> str:
        return hashlib.sha1(value.encode("utf-8")).hexdigest()

    @staticmethod
    def sha256_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    # -------------------------------
    # Random utilities
    # -------------------------------
    @staticmethod
    def random_string(length: int = 12) -> str:
        """Generate random alphanumeric string."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def mask_string(value: str, visible: int = 4) -> str:
        """Mask sensitive string, keeping last `visible` chars visible."""
        if len(value) <= visible:
            return "*" * len(value)
        return "*" * (len(value) - visible) + value[-visible:]


if __name__ == "__main__":
    print("System Info:", Helpers.system_info())
    print("Timestamp:", Helpers.timestamp())
    print("Pretty Time:", Helpers.pretty_time())
    print("MD5 of 'test':", Helpers.md5_hash("test"))
    print("SHA256 of 'test':", Helpers.sha256_hash("test"))
    print("Random string:", Helpers.random_string(8))
    print("Masked string:", Helpers.mask_string("supersecretapikey"))
