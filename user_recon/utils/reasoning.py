# user_recon/util/reasoning.py

from typing import Dict, Any
from difflib import SequenceMatcher
from .entropy import Entropy


class ReasoningEngine:
    """
    Provides AI-style reasoning and human-readable explanations
    for username similarity, entropy levels, and anomaly detection.
    """

    @staticmethod
    def compare_usernames(user1: str, user2: str) -> Dict[str, Any]:
        """
        Compare two usernames and explain similarity.
        Returns dict with similarity %, reasoning, and entropy notes.
        """
        ratio = SequenceMatcher(None, user1, user2).ratio()
        similarity = round(ratio * 100, 2)

        ent1 = Entropy.shannon_entropy(user1)
        ent2 = Entropy.shannon_entropy(user2)

        reasoning = []

        if similarity > 80:
            reasoning.append("Usernames are highly similar, possibly same person.")
        elif similarity > 50:
            reasoning.append("Moderate similarity — could be variant or alias.")
        else:
            reasoning.append("Low similarity — likely different users.")

        if abs(ent1 - ent2) < 0.5:
            reasoning.append("Entropy levels are close, suggesting similar style.")
        else:
            reasoning.append("Entropy difference is large, styles may differ.")

        return {
            "username_1": user1,
            "username_2": user2,
            "similarity_score": similarity,
            "entropy_user1": ent1,
            "entropy_user2": ent2,
            "reasoning": " ".join(reasoning),
        }

    @staticmethod
    def explain_anomaly(username: str, features: Dict[str, Any], status: str) -> str:
        """
        Explain why a username/activity is flagged as anomaly or normal.
        """
        ent = features.get("entropy", 0)
        length = features.get("length", 0)
        specials = features.get("special_char_ratio", 0)

        if status == "Anomaly":
            return (
                f"Username '{username}' flagged as anomaly. "
                f"Entropy={ent}, Length={length}, SpecialChars={specials}. "
                f"Pattern deviates significantly from training distribution."
            )
        else:
            return (
                f"Username '{username}' considered normal. "
                f"Entropy={ent}, Length={length}, SpecialChars={specials}. "
                f"Fits within expected distribution."
            )


if __name__ == "__main__":
    # Demo
    res = ReasoningEngine.compare_usernames("elhamjvdi", "elham87jvdi")
    print(res)

    anomaly_expl = ReasoningEngine.explain_anomaly(
        "X9f!@kPz",
        {"entropy": 4.1, "length": 8, "special_char_ratio": 0.5},
        "Anomaly"
    )
    print(anomaly_expl)
