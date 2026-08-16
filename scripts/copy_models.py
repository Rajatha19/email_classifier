#!/usr/bin/env python3
"""
Script to copy trained ML models from root to backend/models directory.
Run this after training your model in the Jupyter notebook.
"""

import os
import shutil
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
MODEL_FILES = ["best_phishing_model.pkl", "tfidf_vectorizer.pkl"]
SOURCE_DIR = PROJECT_ROOT
DEST_DIR = PROJECT_ROOT / "backend" / "models"

def copy_models():
    """Copy model files from root to backend/models"""
    
    # Ensure destination directory exists
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Copying ML models to {DEST_DIR}...")
    
    copied = 0
    missing = []
    
    for model_file in MODEL_FILES:
        source = SOURCE_DIR / model_file
        dest = DEST_DIR / model_file
        
        if source.exists():
            shutil.copy2(source, dest)
            print(f"✓ Copied {model_file}")
            copied += 1
        else:
            print(f"✗ Missing {model_file} in {SOURCE_DIR}")
            missing.append(model_file)
    
    print(f"\n{copied}/{len(MODEL_FILES)} models copied successfully.")
    
    if missing:
        print(f"\nMissing files: {', '.join(missing)}")
        print("\nPlease run the Jupyter notebook (nlp-based-phishing-detection.ipynb)")
        print("and execute all cells to generate the model files.")
        return 1
    
    print("\n✓ All models ready for deployment!")
    return 0

if __name__ == "__main__":
    exit(copy_models())
