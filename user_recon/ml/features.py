# user_recon/core/features.py

import re
import math
from collections import Counter
import numpy as np


class UsernameFeatureExtractor:
    """
    Extract numeric features from usernames for ML models.
    Features include length, entropy, digit ratio, separators, etc.
    """

    def __init__(self):
        pass

    # -------------------------------
    # Core metrics
    # -------------------------------
    @staticmethod
    def entropy(s: str) -> float:
        """Calculate Shannon entropy of a string."""
        if not s:
            return 0.0
        freq = Counter(s)
        probs = [count / len(s) for count in freq.values()]
        return -sum(p * math.log2(p) for p in probs)

    @staticmethod
    def digit_ratio(s: str) -> float:
        """Return ratio of digits to total length."""
        if not s:
            return 0.0
        return sum(c.isdigit() for c in s) / len(s)

    @staticmethod
    def separator_count(s: str) -> int:
        """Count underscores, dashes, and dots."""
        return sum(s.count(sep) for sep in ["_", "-", "."])

    @staticmethod
    def repeated_char_ratio(s: str) -> float:
        """Measure repeated char density."""
        if not s:
            return 0.0
        repeats = sum(1 for i in range(1, len(s)) if s[i] == s[i - 1])
        return repeats / len(s)

    # -------------------------------
    # Feature extraction
    # -------------------------------
    def extract(self, username: str) -> dict:
        """
        Extract feature dictionary from a single username.
        """
        features = {
            "length": len(username),
            "entropy": round(self.entropy(username), 3),
            "digit_ratio": round(self.digit_ratio(username), 3),
            "separator_count": self.separator_count(username),
            "repeated_char_ratio": round(self.repeated_char_ratio(username), 3),
            "is_lowercase": username.islower(),
            "is_uppercase": username.isupper(),
            "starts_with_digit": username[0].isdigit() if username else False,
        }
        return features

    def to_vector(self, username: str) -> np.ndarray:
        """
        Convert username features to NumPy vector (for ML input).
        """
        feats = self.extract(username)
        return np.array(list(feats.values()), dtype=float)


if __name__ == "__main__":
    extractor = UsernameFeatureExtractor()
    test_usernames = ["elhamjvdi", "admin1234", "xX_dark.lord_99_Xx", "aaaabbb"]

    for u in test_usernames:
        print(f"Username: {u}")
        print("Features:", extractor.extract(u))
        print("Vector:", extractor.to_vector(u))
        print("-" * 50)
