"""Modules 3, 4 and 12: training, evaluation, serialization and MLflow tracking."""
import argparse
import json
import os
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split


def train(input_path: Path, model_dir: Path) -> dict:
    frame = pd.read_csv(input_path)
    x_train, x_test, y_train, y_test = train_test_split(
        frame["text"], frame["target"], test_size=0.2, random_state=42, stratify=frame["target"]
    )
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000, sublinear_tf=True)
    model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    model.fit(vectorizer.fit_transform(x_train), y_train)
    predictions = model.predict(vectorizer.transform(x_test))
    metrics = {
        "f1": float(f1_score(y_test, predictions)), "rows": len(frame),
        "reference_phishing_rate": float(frame["target"].mean()),
        "report": classification_report(y_test, predictions, output_dict=True),
    }
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_dir / "best_phishing_model.pkl")
    joblib.dump(vectorizer, model_dir / "tfidf_vectorizer.pkl")
    (model_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("../data/processed/ceas08_clean.csv"))
    parser.add_argument("--model-dir", type=Path, default=Path("../models"))
    args = parser.parse_args()
    metrics = train(args.input, args.model_dir)
    try:
        import mlflow
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
        mlflow.set_experiment("phishing-email-classifier")
        with mlflow.start_run():
            mlflow.log_params({"algorithm": "LogisticRegression", "vectorizer": "tfidf-1-2gram"})
            mlflow.log_metric("f1", metrics["f1"])
            mlflow.log_artifacts(str(args.model_dir), artifact_path="model")
    except Exception as exc:
        print(f"MLflow tracking skipped: {exc}")
    print(json.dumps({"f1": metrics["f1"], "rows": metrics["rows"]}, indent=2))


if __name__ == "__main__":
    main()
