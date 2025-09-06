# user_recon/util/predictive.py

import re
from typing import List, Dict
from difflib import SequenceMatcher
from .entropy import Entropy


class PredictiveEngine:
    """
    Predictive analysis engine.
    Tries to guess possible variants or aliases of usernames
    and evaluate likelihood of future activity patterns.
    """

    @staticmethod
    def generate_variants(username: str) -> List[str]:
        """
        Generate likely variants of a username (common aliasing tricks).
        """
        variants = []

        # Numeric substitutions
        variants.append(re.sub(r"[aeios]", lambda m: {
            "a": "4", "e": "3", "i": "1", "o": "0", "s": "5"
        }[m.group()], username, flags=re.IGNORECASE))

        # Add random year suffixes
        for year in ["123", "321", "2023", "2024", "99"]:
            variants.append(f"{username}{year}")

        # Underscore or dot separators
        variants.append(username.replace(" ", "_"))
        variants.append(username.replace(" ", "."))
        variants.append(f"_{username}_")

        return list(set(v for v in variants if v != username))

    @staticmethod
    def likelihood_score(user: str, candidate: str) -> Dict[str, float]:
        """
        Estimate likelihood that 'candidate' is an alias of 'user'.
        Uses string similarity + entropy style comparison.
        """
        sim_ratio = SequenceMatcher(None, user, candidate).ratio()
        ent_diff = abs(Entropy.shannon_entropy(user) - Entropy.shannon_entropy(candidate))

        # Combine factors into a probability-style score
        score = (sim_ratio * 0.7 + (1 - ent_diff / 5.0) * 0.3) * 100
        score = max(0.0, min(100.0, round(score, 2)))

        return {
            "user": user,
            "candidate": candidate,
            "similarity": round(sim_ratio * 100, 2),
            "entropy_diff": round(ent_diff, 3),
            "likelihood_score": score
        }

    @staticmethod
    def predict_future_aliases(username: str) -> List[Dict[str, float]]:
        """
        Generate variants and assign likelihood scores for each.
        """
        variants = PredictiveEngine.generate_variants(username)
        return [PredictiveEngine.likelihood_score(username, v) for v in variants]


if __name__ == "__main__":
    test_user = "elhamjvdi"
    print(f"Predicted variants for {test_user}:")
    results = PredictiveEngine.predict_future_aliases(test_user)
    for r in results:
        print(r)
