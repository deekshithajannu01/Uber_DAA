from __future__ import annotations

import re

import numpy as np
import pandas as pd

from .config import CLEAN_FILE
from .ingest import load_raw_dataset


COLUMN_ALIASES = {
    "booking_id": ["booking id", "booking_id", "id"],
    "date": ["date", "booking date"],
    "time": ["time", "booking time"],
    "city": ["city"],
    "pickup_location": ["pickup location", "pickup_location", "pickup"],
    "drop_location": ["drop location", "drop_location", "drop"],
    "vehicle_type": ["vehicle type", "vehicle_type", "cab type"],
    "ride_distance": ["ride distance", "ride_distance", "distance", "trip distance"],
    "booking_value": ["booking value", "booking_value", "fare", "fare amount", "amount"],
    "driver_rating": ["driver ratings", "driver rating", "driver_rating"],
    "customer_rating": ["customer rating", "customer ratings", "customer_rating"],
    "payment_method": ["payment method", "payment_method", "payment"],
    "wait_time": ["wait time", "wait_time", "waiting time", "driver arrival time"],
    "booking_status": ["booking status", "booking_status", "status"],
    "cancelled_by_customer": ["cancelled rides by customer", "cancelled_by_customer"],
    "cancelled_by_driver": ["cancelled rides by driver", "cancelled_by_driver"],
    "customer_cancel_reason": ["reason for cancelling by customer", "customer cancellation reason"],
    "driver_cancel_reason": ["reason for cancelling by driver", "driver cancellation reason"],
}


def _normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized_to_original = {_normalize_name(col): col for col in df.columns}
    rename_map = {}
    for standard, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            original = normalized_to_original.get(_normalize_name(alias))
            if original:
                rename_map[original] = standard
                break
    return df.rename(columns=rename_map)


def _combine_datetime(df: pd.DataFrame) -> pd.Series:
    if "date" in df.columns and "time" in df.columns:
        return pd.to_datetime(df["date"].astype(str) + " " + df["time"].astype(str), errors="coerce")
    if "date" in df.columns:
        return pd.to_datetime(df["date"], errors="coerce")
    return pd.Series(pd.NaT, index=df.index)


def clean_bookings(output_file=CLEAN_FILE) -> pd.DataFrame:
    df = load_raw_dataset()
    df = _rename_columns(df)

    required = ["booking_status", "ride_distance", "booking_value"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns after normalization: {missing}")

    df["booking_datetime"] = _combine_datetime(df)
    df["booking_status"] = df["booking_status"].astype(str).str.strip()
    status_lower = df["booking_status"].str.lower()
    df["is_cancelled"] = status_lower.str.contains("cancel", na=False).astype(int)
    df["is_completed"] = status_lower.str.contains("complete|success", na=False).astype(int)

    numeric_cols = ["ride_distance", "booking_value", "driver_rating", "customer_rating", "wait_time"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["city", "pickup_location", "drop_location", "vehicle_type", "payment_method"]:
        if col not in df.columns:
            df[col] = "Unknown"
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()

    if "wait_time" not in df.columns:
        df["wait_time"] = np.nan
    if "driver_rating" not in df.columns:
        df["driver_rating"] = np.nan
    if "customer_rating" not in df.columns:
        df["customer_rating"] = np.nan

    df = df[
        df["ride_distance"].notna()
        & df["booking_value"].notna()
        & (df["ride_distance"] >= 0)
        & (df["booking_value"] >= 0)
    ].copy()

    df["hour"] = df["booking_datetime"].dt.hour.fillna(-1).astype(int)
    df["day_of_week"] = df["booking_datetime"].dt.dayofweek.fillna(-1).astype(int)
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["is_peak_hour"] = df["hour"].isin([8, 9, 10, 17, 18, 19, 20, 21]).astype(int)
    df["fare_per_km"] = np.where(df["ride_distance"] > 0, df["booking_value"] / df["ride_distance"], 0)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Saved cleaned bookings: {output_file} ({len(df):,} rows)")
    print(f"Cancellation rate: {df['is_cancelled'].mean():.2%}")
    return df


if __name__ == "__main__":
    clean_bookings()
