"""Module 2: concise EDA report suitable for a reproducible project submission."""
import argparse
from pathlib import Path
import pandas as pd
from training.features import engineered_features


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("input", type=Path); args = parser.parse_args()
    data = pd.read_csv(args.input)
    features = pd.DataFrame([engineered_features(value) for value in data["text"].fillna("")])
    print("Label distribution:\n", data["target"].value_counts(normalize=True).rename("share"))
    print("\nFeature summary:\n", features.describe().T)


if __name__ == "__main__":
    main()
