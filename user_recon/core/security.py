# user_recon/core/security.py

import hashlib
import re
import time
import threading
from collections import defaultdict


class SecurityUtils:
    """
    Security utilities for User Recon.
    Provides sanitization, hashing, API key protection,
    and simple rate-limiting + anomaly detection.
    """

    # Regex patterns for suspicious input
    SQLI_PATTERN = re.compile(r"(?:')|(?:--)|(/\*)|(\*/)|(;)|(\b(OR|AND)\b)", re.IGNORECASE)
    XSS_PATTERN = re.compile(r"<script.*?>.*?</script.*?>", re.IGNORECASE)

    def __init__(self):
        self.api_keys = {}
        self.request_log = defaultdict(list)
        self.lock = threading.Lock()

    # -------------------------------
    # Hashing Utilities
    # -------------------------------
    @staticmethod
    def hash_value(value: str) -> str:
        """Return SHA-256 hash of a given value."""
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    # -------------------------------
    # Input Validation & Sanitization
    # -------------------------------
    def sanitize_input(self, text: str) -> str:
        """
        Basic input sanitization against SQLi/XSS.
        Returns safe version if suspicious patterns are found.
        """
        if self.SQLI_PATTERN.search(text) or self.XSS_PATTERN.search(text):
            return re.sub(r"[^a-zA-Z0-9._-]", "", text)
        return text

    def validate_username(self, username: str) -> bool:
        """Allow only alphanumeric, underscore, dot, and dash."""
        return bool(re.match(r"^[a-zA-Z0-9._-]{3,32}$", username))

    # -------------------------------
    # API Key Vault
    # -------------------------------
    def store_api_key(self, service: str, key: str):
        """Securely store API key (hashed for audit)."""
        with self.lock:
            self.api_keys[service] = self.hash_value(key)

    def verify_api_key(self, service: str, key: str) -> bool:
        """Verify API key against stored hash."""
        with self.lock:
            if service not in self.api_keys:
                return False
            return self.api_keys[service] == self.hash_value(key)

    # -------------------------------
    # Rate Limiting
    # -------------------------------
    def rate_limit(self, user_id: str, limit: int = 10, window: int = 60) -> bool:
        """
        Simple rate limiting.
        - limit: max requests
        - window: seconds
        Returns True if allowed, False if blocked.
        """
        now = time.time()
        with self.lock:
            self.request_log[user_id] = [
                ts for ts in self.request_log[user_id] if ts > now - window
            ]
            if len(self.request_log[user_id]) >= limit:
                return False
            self.request_log[user_id].append(now)
            return True

    # -------------------------------
    # Suspicious Behavior Detection
    # -------------------------------
    def detect_suspicious_activity(self, username: str) -> list:
        """
        Detect risky patterns in usernames (security-focused).
        Returns list of warnings.
        """
        warnings = []
        if re.search(r"(password|passwd|login)", username.lower()):
            warnings.append("Username contains credential-like keywords.")
        if re.match(r"^\d+$", username):
            warnings.append("Username is numeric only, likely bot or spam.")
        if len(username) > 30:
            warnings.append("Excessively long username, suspicious behavior.")
        return warnings


if __name__ == "__main__":
    sec = SecurityUtils()
    # Demo
    test_usernames = ["admin123", "safe_user", "<script>alert(1)</script>", "12345678"]
    for u in test_usernames:
        print(f"Testing {u}")
        print("Sanitized:", sec.sanitize_input(u))
        print("Valid?:", sec.validate_username(u))
        print("Suspicious:", sec.detect_suspicious_activity(u))
        print("-" * 40)
