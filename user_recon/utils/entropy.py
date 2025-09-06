# user_recon/util/entropy.py

import math
from collections import Counter


class Entropy:
    """
    Entropy utilities for analyzing randomness of strings.
    Useful for usernames, tokens, API keys, or suspicious data.
    """

    @staticmethod
    def shannon_entropy(text: str) -> float:
        """
        Calculate Shannon entropy of a string.
        Higher values = more random/unpredictable.
        """
        if not text:
            return 0.0

        counts = Counter(text)
        length = len(text)

        entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
        return round(entropy, 4)

    @staticmethod
    def normalized_entropy(text: str) -> float:
        """
        Normalize entropy to [0, 1] scale.
        0 = fully predictable, 1 = maximum randomness.
        """
        if not text:
            return 0.0

        max_entropy = math.log2(len(set(text)))
        if max_entropy == 0:
            return 0.0

        return round(Entropy.shannon_entropy(text) / max_entropy, 4)

    @staticmethod
    def classify_entropy(text: str) -> str:
        """
        Human-friendly classification of entropy level.
        """
        ent = Entropy.shannon_entropy(text)

        if ent < 2.5:
            return "Low (predictable)"
        elif ent < 4.0:
            return "Medium (balanced)"
        else:
            return "High (random/complex)"


if __name__ == "__main__":
    samples = [
        "admin",
        "elhamjvdi",
        "elham87jvdi",
        "X9f!@kPz",
        "aaaaaaaaaa",
        "qwerty123",
    ]

    for s in samples:
        print(
            f"{s:12} | Entropy: {Entropy.shannon_entropy(s)} "
            f"| Normalized: {Entropy.normalized_entropy(s)} "
            f"| Class: {Entropy.classify_entropy(s)}"
        )
