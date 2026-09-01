from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import RAW_CANDIDATES, RAW_DIR


def find_raw_dataset() -> Path:
    """Find the ride-booking CSV placed in data/raw."""
    for filename in RAW_CANDIDATES:
        path = RAW_DIR / filename
        if path.exists():
            return path

    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if csv_files:
        return csv_files[0]

    raise FileNotFoundError(
        "No raw CSV found in data/raw. Download the Kaggle ride booking dataset "
        "and place it there, or run sample_data.py to generate a demo dataset."
    )


def load_raw_dataset() -> pd.DataFrame:
    path = find_raw_dataset()
    print(f"Loading raw dataset: {path}")
    return pd.read_csv(path)
