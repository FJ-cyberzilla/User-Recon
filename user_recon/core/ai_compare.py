# user_recon/core/ai_compare.py

import re
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class AIUsernameComparator:
    """
    AI-powered username comparator.
    Uses hybrid logic: string similarity + ML vectorization.
    Returns similarity percentage + human-readable reasoning.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))

    def normalize(self, username: str) -> str:
        """Normalize username for comparison."""
        return re.sub(r"[^a-z0-9]", "", username.lower())

    def sequence_score(self, u1: str, u2: str) -> float:
        """Compute ratio using SequenceMatcher."""
        return SequenceMatcher(None, u1, u2).ratio()

    def tfidf_score(self, u1: str, u2: str) -> float:
        """Compute cosine similarity using TF-IDF vectorization."""
        matrix = self.vectorizer.fit_transform([u1, u2])
        return cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    def compare(self, user1: str, user2: str, results1=None, results2=None) -> dict:
        """
        Compare two usernames and optionally their social media results.
        Returns dict with similarity % and reasoning.
        """

        norm1, norm2 = self.normalize(user1), self.normalize(user2)

        seq_score = self.sequence_score(norm1, norm2)
        tfidf_score = self.tfidf_score(norm1, norm2)

        base_score = (seq_score * 0.5 + tfidf_score * 0.5) * 100

        # Boost if many shared platforms
        shared_platforms = 0
        total_checked = 0
        if results1 and results2:
            for site in results1:
                if site in results2:
                    total_checked += 1
                    if (
                        results1[site][0] is True
                        and results2[site][0] is True
                    ):
                        shared_platforms += 1
            if total_checked > 0:
                platform_score = (shared_platforms / total_checked) * 30
                base_score = min(100, base_score + platform_score)

        # Human reasoning
        reasoning_parts = []
        if norm1 == norm2:
            reasoning_parts.append("Both usernames are identical after normalization.")
        elif seq_score > 0.8:
            reasoning_parts.append("They share a very strong character sequence overlap.")
        elif seq_score > 0.5:
            reasoning_parts.append("There is partial similarity in character sequence.")
        else:
            reasoning_parts.append("The usernames have weak structural similarity.")

        if tfidf_score > 0.7:
            reasoning_parts.append("Statistical analysis shows high contextual similarity.")
        elif tfidf_score > 0.4:
            reasoning_parts.append("There is moderate contextual similarity.")
        else:
            reasoning_parts.append("Contextual similarity is low.")

        if results1 and results2:
            reasoning_parts.append(
                f"Both appear on {shared_platforms} shared platforms out of {total_checked} checked."
            )

        if base_score >= 80:
            verdict = "Highly likely same user"
        elif base_score >= 60:
            verdict = "Possibly same user"
        else:
            verdict = "Unlikely same user"

        return {
            "username1": user1,
            "username2": user2,
            "similarity_score": round(base_score, 2),
            "verdict": verdict,
            "reasoning": " ".join(reasoning_parts),
        }


if __name__ == "__main__":
    # Quick test
    comparator = AIUsernameComparator()
    result = comparator.compare("elhamjvdi", "elham87jvdi")
    print(result)
