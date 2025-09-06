# user_recon/core/trainer.py

import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class UsernameTrainer:
    """
    Train and persist models for username similarity & classification.
    Uses TF-IDF + Logistic Regression for practical results.
    """

    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
        self.sim_model_path = os.path.join(self.model_dir, "username_similarity.pkl")
        self.clf_model_path = os.path.join(self.model_dir, "username_classifier.pkl")

        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))

    # ------------------------------------------------
    # Similarity Model
    # ------------------------------------------------
    def train_similarity(self, usernames: list):
        """
        Train and save TF-IDF matrix for similarity comparisons.
        usernames: list of usernames to build vocabulary.
        """
        tfidf_matrix = self.vectorizer.fit_transform(usernames)
        joblib.dump((self.vectorizer, tfidf_matrix), self.sim_model_path)
        return {"status": "trained", "model": self.sim_model_path}

    def compare_usernames(self, u1: str, u2: str) -> float:
        """
        Compare two usernames using cosine similarity.
        Returns similarity percentage.
        """
        if not os.path.exists(self.sim_model_path):
            raise RuntimeError("Similarity model not trained. Run train_similarity() first.")
        vectorizer, _ = joblib.load(self.sim_model_path)
        tfidf = vectorizer.transform([u1, u2])
        sim = cosine_similarity(tfidf[0], tfidf[1])[0][0]
        return round(sim * 100, 2)

    # ------------------------------------------------
    # Classification Model
    # ------------------------------------------------
    def train_classifier(self, usernames: list, labels: list):
        """
        Train classifier on usernames.
        labels: e.g. ["personal", "bot", "generic"]
        """
        clf_pipeline = Pipeline([
            ("vectorizer", TfidfVectorizer(analyzer="char", ngram_range=(2, 4))),
            ("clf", LogisticRegression(max_iter=500))
        ])
        clf_pipeline.fit(usernames, labels)
        joblib.dump(clf_pipeline, self.clf_model_path)
        return {"status": "trained", "model": self.clf_model_path}

    def predict_label(self, username: str) -> dict:
        """
        Predict label for a username.
        Returns {label, confidence}.
        """
        if not os.path.exists(self.clf_model_path):
            raise RuntimeError("Classifier model not trained. Run train_classifier() first.")
        clf_pipeline = joblib.load(self.clf_model_path)
        probs = clf_pipeline.predict_proba([username])[0]
        label = clf_pipeline.classes_[np.argmax(probs)]
        confidence = round(np.max(probs) * 100, 2)
        return {"username": username, "label": label, "confidence": confidence}


if __name__ == "__main__":
    trainer = UsernameTrainer()

    # Demo usernames
    demo_usernames = ["elhamjvdi", "admin123", "test_user", "bot9999", "xXcoolguyXx"]
    demo_labels = ["personal", "generic", "generic", "bot", "personal"]

    print("Training similarity model...")
    print(trainer.train_similarity(demo_usernames))

    print("Comparing elhamjvdi vs elham87jvdi...")
    print(trainer.compare_usernames("elhamjvdi", "elham87jvdi"))

    print("Training classifier...")
    print(trainer.train_classifier(demo_usernames, demo_labels))

    print("Predicting label for 'admin123'...")
    print(trainer.predict_label("admin123"))
