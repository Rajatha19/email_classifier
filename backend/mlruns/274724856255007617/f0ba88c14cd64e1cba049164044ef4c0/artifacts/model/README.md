# ML Models Directory

This directory should contain the trained machine learning models for email classification.

## Required Files

1. `best_phishing_model.pkl` - The trained scikit-learn model (Naive Bayes, SVM, or Random Forest)
2. `tfidf_vectorizer.pkl` - The TF-IDF vectorizer used to transform email text

## How to Generate Models

Run the Jupyter notebook at the root of the project:
```bash
jupyter notebook nlp-based-phishing-detection.ipynb
```

Execute all cells in the notebook. The last cell will save:
- `best_phishing_model.pkl`
- `tfidf_vectorizer.pkl`

## Copying Models to Backend

After training, copy the model files to this directory:

```bash
# From the project root
cp best_phishing_model.pkl backend/models/
cp tfidf_vectorizer.pkl backend/models/
```

Or use the provided script:
```bash
# From the email-classifier-monorepo directory
python scripts/copy_models.py
```

## Model Information

The ML classifier expects:
- Input: Email text (subject + body combined and lowercased)
- Output: Binary classification (0 = legitimate/productive, 1 = phishing/unproductive)
- Preprocessing: TF-IDF vectorization with English stop words, bigrams (1,2)

## Docker

When building the Docker image, these model files will be copied into the container automatically.
Ensure the model files exist in this directory before building.
