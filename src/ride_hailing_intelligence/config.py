from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

RAW_CANDIDATES = [
    "ola_uber_ride_bookings.csv",
    "ola_uber_bookings.csv",
    "ncr_ride_bookings.csv",
    "ride_bookings.csv",
    "bookings.csv",
]

SAMPLE_RAW_FILE = RAW_DIR / "sample_ride_bookings.csv"
CLEAN_FILE = PROCESSED_DIR / "clean_ride_bookings.csv"
FEATURE_FILE = PROCESSED_DIR / "modeling_dataset.csv"
