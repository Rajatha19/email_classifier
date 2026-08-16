# ML Model Integration - Setup Guide

This guide explains how to use your trained machine learning model instead of OpenAI for email classification.

## Overview

The backend now supports three classification methods (in priority order):
1. **ML Model** (scikit-learn) - Default, no API costs
2. **OpenAI** - Fallback option, requires API key
3. **Rule-based** - Simple keyword matching

## Quick Start

### 1. Train Your Model

First, train the model using the Jupyter notebook:

```bash
cd email-classifier-monorepo
jupyter notebook nlp-based-phishing-detection.ipynb
```

Run all cells in the notebook. The last cell will generate:
- `best_phishing_model.pkl`
- `tfidf_vectorizer.pkl`

### 2. Copy Models to Backend

Run the copy script:

```bash
python scripts/copy_models.py
```

Or manually:

```bash
cp best_phishing_model.pkl backend/models/
cp tfidf_vectorizer.pkl backend/models/
```

### 3. Configure Environment

Update your `.env` file (or copy from `.env.example`):

```env
# Enable ML Model (default)
USE_ML_MODEL=true

# Disable OpenAI (optional fallback)
USE_OPENAI=false
OPENAI_API_KEY=your-key-here
```

### 4. Run Locally (Without Docker)

```bash
cd backend
pip install -r requirements.txt
python -m scripts.seed_if_empty
uvicorn app.main:app --reload --port 8044
```

### 5. Run with Docker

Build the Docker image:

```bash
cd backend
docker build -t email-classifier-backend .
```

Run the container:

```bash
docker run -p 8044:8044 \
  -e USE_ML_MODEL=true \
  -e USE_OPENAI=false \
  email-classifier-backend
```

Or use docker-compose:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8044:8044"
    environment:
      - USE_ML_MODEL=true
      - USE_OPENAI=false
      - ALLOW_ORIGINS=http://localhost:3000
    volumes:
      - ./backend/data.db:/app/data.db
```

## Testing the API

### Test with curl

```bash
# Test with a sample email
curl -X POST http://localhost:8044/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Important meeting tomorrow",
    "body": "Hi, can we schedule a meeting to discuss the project?",
    "sender": "colleague@company.com"
  }'
```

### Expected Response

```json
{
  "category": "productive",
  "reason": "ML model classified as legitimate email (confidence: 0.85)",
  "suggested_reply": "Hello colleague@company.com,\n\nThank you for your email about 'Important meeting tomorrow'...",
  "used_model": "ml_classifier",
  "extra": {
    "confidence": 0.85,
    "ml_prediction": 0,
    "model_type": "MultinomialNB"
  }
}
```

## Architecture

### File Structure

```
backend/
├── app/
│   ├── infrastructure/
│   │   └── classifiers/
│   │       ├── ml_classifier.py      ← NEW: ML-based classifier
│   │       ├── openai_llm.py         ← Existing: OpenAI classifier
│   │       ├── rule_based.py         ← Existing: Keyword-based
│   │       └── smart_classifier.py   ← Existing: Hybrid approach
│   ├── bootstrap.py                   ← UPDATED: ML priority
│   └── config.py                      ← UPDATED: ML settings
├── models/                            ← NEW: Model storage
│   ├── best_phishing_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── README.md
├── requirements.txt                   ← UPDATED: Added scikit-learn
└── Dockerfile                         ← UPDATED: Copy models/
```

### How It Works

1. **MLClassifier** loads the trained model and vectorizer on initialization
2. Email text (subject + body) is preprocessed (lowercased)
3. TF-IDF vectorizer transforms text to feature vectors
4. Model predicts: 0 = productive, 1 = unproductive/phishing
5. Confidence score is extracted from probability or decision function
6. Result includes category, reason, and suggested reply

### Fallback Strategy

The system tries classifiers in this order:

1. If `USE_ML_MODEL=true` → Try ML classifier
   - If loading fails → Fall back to next option
2. If `USE_OPENAI=true` → Try OpenAI classifier
3. Otherwise → Use rule-based classifier

## Model Details

### Training Data
- Dataset: `phishing_email.csv`
- Features: TF-IDF vectors with bigrams (1,2)
- Stop words: English
- Models tested: Naive Bayes, SVM, Random Forest

### Classification Logic

```python
# Prediction mapping
0 → Category.PRODUCTIVE (legitimate email)
1 → Category.UNPRODUCTIVE (phishing/spam)
```

### Confidence Scores

- **Probabilistic models** (Naive Bayes, Random Forest): Uses `predict_proba()`
- **SVM**: Uses `decision_function()` absolute value
- Higher confidence = more certain prediction

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_ML_MODEL` | `true` | Enable ML classifier |
| `ML_MODEL_PATH` | `./models/best_phishing_model.pkl` | Custom model path |
| `ML_VECTORIZER_PATH` | `./models/tfidf_vectorizer.pkl` | Custom vectorizer path |
| `USE_OPENAI` | `false` | Enable OpenAI fallback |
| `OPENAI_API_KEY` | - | OpenAI API key |

## Troubleshooting

### Model Not Found Error

```
RuntimeError: Could not load ML classifier
```

**Solution**: Ensure model files exist in `backend/models/`:
```bash
ls -la backend/models/
# Should show:
# best_phishing_model.pkl
# tfidf_vectorizer.pkl
```

### scikit-learn Version Mismatch

```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution**: Install requirements:
```bash
pip install -r requirements.txt
```

### Docker Build Fails

```
COPY failed: file not found in build context
```

**Solution**: Ensure models exist before building:
```bash
python scripts/copy_models.py
docker build -t email-classifier-backend ./backend
```

## Performance Comparison

| Method | Speed | Cost | Accuracy | Offline |
|--------|-------|------|----------|---------|
| ML Model | ⚡ Fast (~50ms) | 💰 Free | ✓ Good | ✅ Yes |
| OpenAI | 🐌 Slow (~2s) | 💸 $$$ | ✓✓ Better | ❌ No |
| Rule-based | ⚡⚡ Fastest (~10ms) | 💰 Free | ⚠️ Basic | ✅ Yes |

## Next Steps

1. **Improve Model**: Retrain with more data for better accuracy
2. **Monitor Performance**: Track predictions and adjust threshold
3. **A/B Testing**: Compare ML vs OpenAI on real data
4. **Deploy**: Use in production with Docker/Kubernetes

## Support

For issues or questions:
- Check logs: `docker logs <container-id>`
- Review model training: See notebook cell outputs
- Test locally: Run without Docker first
