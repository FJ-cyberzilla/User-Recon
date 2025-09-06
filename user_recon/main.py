# main.py

import argparse
import json
from datetime import datetime

from user_recon.core.search import SocialSearch
from user_recon.util.entropy import Entropy
from user_recon.util.anomaly import AnomalyDetector
from user_recon.util.reasoning import ReasoningEngine
from user_recon.util.predictive import PredictiveEngine
from user_recon.util.logging import Logger


def run_user_recon(username: str, verbose: bool = False) -> dict:
    """
    Orchestrates full User Recon pipeline:
    - Social media search
    - Entropy analysis
    - Similarity reasoning
    - Predictive alias generation
    - Anomaly detection
    """

    results = {
        "username": username,
        "timestamp": datetime.utcnow().isoformat(),
        "analysis": {}
    }

    # 1. Social search
    Logger.info(f"Searching platforms for '{username}'...")
    search = SocialSearch(username)
    social_results = search.run_search()

    results["analysis"]["social_presence"] = social_results

    # 2. Entropy analysis
    entropy_val = Entropy.shannon_entropy(username)
    norm_entropy = Entropy.normalized_entropy(username)
    entropy_class = Entropy.classify_entropy(username)

    results["analysis"]["entropy"] = {
        "raw": entropy_val,
        "normalized": norm_entropy,
        "class": entropy_class
    }

    # 3. Predictive aliases
    Logger.info("Generating predictive aliases...")
    predictions = PredictiveEngine.predict_future_aliases(username)
    results["analysis"]["predicted_aliases"] = predictions

    # 4. Anomaly detection (fit with simple features from predictions)
    Logger.info("Running anomaly detection...")
    detector = AnomalyDetector(contamination=0.15)
    features = [[p["similarity"], len(p["candidate"]), p["entropy_diff"]] for p in predictions]
    detector.fit(features)

    anomaly_statuses = detector.batch_predict(features)
    anomaly_explanations = [
        ReasoningEngine.explain_anomaly(
            p["candidate"],
            {"entropy": Entropy.shannon_entropy(p["candidate"]),
             "length": len(p["candidate"]),
             "special_char_ratio": sum(not c.isalnum() for c in p["candidate"]) / max(1, len(p["candidate"]))},
            status
        )
        for p, status in zip(predictions, anomaly_statuses)
    ]

    results["analysis"]["anomaly_reports"] = anomaly_explanations

    # Final summary
    Logger.success("Recon complete.")
    return results


def cli():
    parser = argparse.ArgumentParser(description="User Recon - AI-driven OSINT tool for usernames")
    parser.add_argument("username", help="Target username to analyze")
    parser.add_argument("-o", "--output", help="Save results to JSON file", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()
    Logger.verbose = args.verbose

    report = run_user_recon(args.username, verbose=args.verbose)

    # Print to console
    print(json.dumps(report, indent=4))

    # Save if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=4)
        Logger.info(f"Results saved to {args.output}")


if __name__ == "__main__":
    cli()
