"""Small Prometheus instrumentation layer, safe to import in every deployment."""
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from fastapi.responses import Response

CLASSIFICATIONS = Counter(
    "phishing_classifications_total", "Classifications by result", ["category", "model"]
)
CLASSIFICATION_LATENCY = Histogram(
    "phishing_classification_latency_seconds", "Classification latency in seconds"
)
MODEL_LOAD_FAILURES = Counter("phishing_model_load_failures_total", "Model artifact load failures")


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
