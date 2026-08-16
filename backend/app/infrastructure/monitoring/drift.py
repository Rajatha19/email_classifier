"""Lightweight, dependency-free prediction drift monitor.

It compares the rolling phishing rate with a reference rate using a z-score.
This is intended as a deployable baseline; scheduled retraining should be
reviewed by a human rather than triggered automatically.
"""
from collections import deque
from math import sqrt


class PredictionDriftMonitor:
    def __init__(self, reference_rate: float = 0.5, window_size: int = 200):
        self.reference_rate = reference_rate
        self.window_size = window_size
        self.values: deque[int] = deque(maxlen=window_size)

    def record(self, is_phishing: bool) -> None:
        self.values.append(int(is_phishing))

    def report(self) -> dict:
        count = len(self.values)
        if count < 30:
            return {"status": "insufficient_data", "samples": count, "drift_detected": False}
        rate = sum(self.values) / count
        variance = max(self.reference_rate * (1 - self.reference_rate), 0.0001)
        z_score = abs(rate - self.reference_rate) / sqrt(variance / count)
        return {
            "status": "ok", "samples": count, "current_phishing_rate": round(rate, 4),
            "reference_phishing_rate": self.reference_rate, "z_score": round(z_score, 3),
            "drift_detected": z_score >= 3.0,
        }


drift_monitor = PredictionDriftMonitor()
