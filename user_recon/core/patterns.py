# user_recon/core/patterns.py

import re
import math
from collections import Counter


class UsernamePatternAnalyzer:
    """
    Analyze username patterns with rule-based heuristics
    + entropy scoring for complexity evaluation.
    """

    GENERIC_KEYWORDS = [
        "admin", "root", "test", "user", "support",
        "info", "contact", "guest", "service"
    ]

    def __init__(self):
        pass

    def entropy(self, s: str) -> float:
        """Calculate Shannon entropy of a string."""
        if not s:
            return 0.0
        freq = Counter(s)
        probs = [count / len(s) for count in freq.values()]
        return -sum(p * math.log2(p) for p in probs)

    def analyze(self, username: str) -> dict:
        """
        Analyze username and return insights.
        """

        u = username.lower()
        reasoning = []

        # Generic/role-based detection
        if any(keyword in u for keyword in self.GENERIC_KEYWORDS):
            reasoning.append("Contains generic or role-based keyword.")

        # Short username
        if len(u) <= 5:
            reasoning.append("Very short username, likely personal or early adopter.")

        # Numbers
        digit_count = sum(c.isdigit() for c in u)
        if digit_count > 3:
            reasoning.append("Contains many digits, possible auto-generated or spammy.")
        elif 1 <= digit_count <= 3:
            reasoning.append("Contains digits, maybe birth year or lucky numbers.")

        # Separators
        if "_" in u or "." in u or "-" in u:
            reasoning.append("Uses separators (underscore/dot/dash), common in personal accounts.")

        # Repeated characters
        if re.search(r"(.)\1{2,}", u):
            reasoning.append("Has repeated characters, maybe stylized or bot-generated.")

        # Entropy score
        ent = self.entropy(u)
        if ent < 2.5:
            reasoning.append("Low entropy: predictable, simple structure.")
        elif ent < 3.5:
            reasoning.append("Moderate entropy: balanced complexity.")
        else:
            reasoning.append("High entropy: complex or random structure.")

        # Default reasoning if nothing triggered
        if not reasoning:
            reasoning.append("No obvious patterns detected; likely personal account.")

        # Verdict based on signals
        if any("generic" in r.lower() for r in reasoning):
            verdict = "Generic/role-based"
        elif digit_count > 3 or "random" in "".join(reasoning).lower():
            verdict = "Possibly automated"
        else:
            verdict = "Likely personal"

        return {
            "username": username,
            "entropy": round(ent, 2),
            "signals": reasoning,
            "verdict": verdict
        }


if __name__ == "__main__":
    analyzer = UsernamePatternAnalyzer()
    test_usernames = ["elhamjvdi", "admin1234", "xX_dark.lord_99_Xx", "aaaabbb"]
    for u in test_usernames:
        print(analyzer.analyze(u))
