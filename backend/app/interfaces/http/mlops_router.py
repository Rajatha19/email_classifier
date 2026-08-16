"""MLOps endpoints: model visibility, drift status, and optional Kafka inference."""
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.bootstrap import build_use_case
from app.infrastructure.monitoring.drift import drift_monitor

router = APIRouter(prefix="/mlops")


class StreamEmail(BaseModel):
    subject: str = Field(default="", max_length=500)
    body: str = Field(min_length=1, max_length=20000)
    sender: str | None = None


@router.get("/model")
def model_info():
    backend_root = Path(__file__).resolve().parents[3]
    model = backend_root / "models" / "best_phishing_model.pkl"
    vectorizer = backend_root / "models" / "tfidf_vectorizer.pkl"
    return {
        "name": "tfidf-phishing-classifier", "artifacts_present": model.exists() and vectorizer.exists(),
        "model_path": str(model), "tracking_uri": os.getenv("MLFLOW_TRACKING_URI", "local ./mlruns"),
    }


@router.get("/drift")
def drift_status():
    return drift_monitor.report()


@router.post("/stream/classify")
def stream_classify(payload: StreamEmail):
    """Synchronous endpoint used by Kafka consumers and dashboard demos."""
    try:
        result = build_use_case().execute_from_text(payload.subject, payload.body, payload.sender)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to classify stream message") from exc
    drift_monitor.record(str(result.category.value) == "unproductive")
    return result.__dict__
