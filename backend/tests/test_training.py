from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from training.features import engineered_features
from app.infrastructure.monitoring.drift import PredictionDriftMonitor


def test_engineered_features_detects_urls_and_terms():
    features = engineered_features("URGENT: verify account at https://example.test/login!")
    assert features["url_count"] == 1
    assert features["suspicious_term_count"] >= 2


def test_drift_monitor_requires_minimum_observations():
    monitor = PredictionDriftMonitor(reference_rate=0.5)
    monitor.record(True)
    assert monitor.report()["status"] == "insufficient_data"
