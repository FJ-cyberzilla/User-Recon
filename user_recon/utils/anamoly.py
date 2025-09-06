# user_recon/util/anomaly.py

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Dict


class AnomalyDetector:
    """
    Anomaly detection for usernames and activity patterns.
    Uses Isolation Forest (unsupervised ML) to detect outliers.
    """

    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, features: List[List[float]]):
        """
        Fit anomaly detector on a batch of feature vectors.
        """
        X = np.array(features)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_fitted = True

    def predict(self, features: List[float]) -> str:
        """
        Predict if a single feature vector is anomalous.
        Returns: "Normal" or "Anomaly"
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")

        X_scaled = self.scaler.transform([features])
        pred = self.model.predict(X_scaled)[0]
        return "Normal" if pred == 1 else "Anomaly"

    def batch_predict(self, features: List[List[float]]) -> List[str]:
        """
        Predict anomalies for a batch of feature vectors.
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")

        X_scaled = self.scaler.transform(features)
        preds = self.model.predict(X_scaled)
        return ["Normal" if p == 1 else "Anomaly" for p in preds]


if __name__ == "__main__":
    # Demo usage
    sample_features = [
        [0.3, 5, 0.6],   # Normal
        [0.4, 6, 0.55],  # Normal
        [10.0, 50, 0.99] # Outlier
    ]

    detector = AnomalyDetector(contamination=0.15)
    detector.fit(sample_features)

    print("Batch prediction:", detector.batch_predict(sample_features))
    print("Single:", detector.predict([0.35, 5.5, 0.58]))
