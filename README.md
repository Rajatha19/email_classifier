# Phishing Email Detection Platform

This project has been extended into a full MLOps phishing-email classifier using the supplied CEAS-08 dataset. It keeps the original FastAPI/React email experience while adding reproducible training, model operations, streaming, and deployment tooling.

## Requested modules

| Module | Implementation |
| --- | --- |
| 1. Data acquisition & preprocessing | `backend/training/prepare_data.py`; supplied CSV is placed in `data/raw/` |
| 2. Feature engineering & EDA | `backend/training/features.py` and `backend/training/eda.py` |
| 3. Model development & training | TF-IDF + class-balanced Logistic Regression in `backend/training/train.py` |
| 4. Serialization & explainability | joblib model/vectorizer artifacts; prediction confidence and reason returned by API |
| 5. FastAPI | `/classify`, `/logs`, `/mlops/model`, `/mlops/drift`, `/mlops/stream/classify`, `/metrics` |
| 6. Docker | Backend/frontend Dockerfiles and `docker-compose.yml` |
| 7. Monitoring & logging | Prometheus metrics plus SQLite classification audit logs |
| 8. React dashboard | Existing classification UI plus `MLOpsDashboard` model/drift panel |
| 9. CI/CD | GitHub Actions workflow at `.github/workflows/ci.yml` |
| 10. Kafka streaming | `backend/streaming/consumer.py` and Kafka service configuration |
| 11. Model drift | Rolling phishing-rate z-score detector exposed through `/mlops/drift` |
| 12. MLflow experiment tracking | Training run logs parameters, F1, and artifacts to MLflow when configured |

## First run

Use Python 3.12 (or 3.10+) and Node 20. From `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m training.prepare_data --input ..\data\raw\CEAS_08.csv --output ..\data\processed\ceas08_clean.csv
python -m training.eda ..\data\processed\ceas08_clean.csv
python -m training.train --input ..\data\processed\ceas08_clean.csv --model-dir .\models
uvicorn app.main:app --reload --port 8044
```

In another terminal, run the React dashboard:

```powershell
cd frontend
npm ci
npm run dev
```

The dashboard is at `http://localhost:3000`; API documentation is at `http://localhost:8044/docs`.

## Containers and optional services

Run `docker compose up --build` from the repository root to start the API, React dashboard, Kafka and MLflow. The API works without Kafka or MLflow for local development. To use Kafka inference, start `python -m streaming.consumer` after creating/feeding the `incoming-emails` topic. Messages have `subject`, `body`, and optional `sender` fields.

MLflow defaults to a local `mlruns` directory. Set `MLFLOW_TRACKING_URI=http://localhost:5000` to log to the Docker MLflow service instead.

## Dataset handling

`CEAS_08.csv` is intentionally ignored by Git because it is data, not source code. The source schema expected by preprocessing is `sender, receiver, date, subject, body, label, urls`. Never send live email bodies or credentials to the public MLflow/Kafka services without applying your organisation's privacy controls.
