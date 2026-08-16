"""Module 1: turn the CEAS-08 source CSV into a clean training table.

Run from backend: python -m training.prepare_data --input ../data/raw/CEAS_08.csv
"""
import argparse
from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {"subject", "body", "label"}


def clean_dataset(source: Path) -> pd.DataFrame:
    data = pd.read_csv(source, on_bad_lines="skip")
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    data = data.dropna(subset=["label"]).copy()
    data["subject"] = data["subject"].fillna("").astype(str)
    data["body"] = data["body"].fillna("").astype(str)
    data["text"] = (data["subject"] + " " + data["body"]).str.replace(r"\s+", " ", regex=True).str.strip()
    data = data[data["text"].str.len() > 0].copy()
    # CEAS labels are commonly 0=ham and 1=spam; normalise robustly for either form.
    data["target"] = data["label"].astype(str).str.lower().isin({"1", "spam", "phishing", "true"}).astype(int)
    return data[["text", "target", "subject", "body", "urls"]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("../data/processed/ceas08_clean.csv"))
    args = parser.parse_args()
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    clean_dataset(args.input).to_csv(output, index=False)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
