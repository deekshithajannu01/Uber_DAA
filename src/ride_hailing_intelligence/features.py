from __future__ import annotations

import pandas as pd

from .config import CLEAN_FILE, FEATURE_FILE


def build_features(input_file=CLEAN_FILE, output_file=FEATURE_FILE) -> pd.DataFrame:
    df = pd.read_csv(input_file, parse_dates=["booking_datetime"])

    group_cols = ["city", "pickup_location", "vehicle_type"]
    segment_stats = (
        df.groupby(group_cols)
        .agg(
            segment_bookings=("booking_status", "size"),
            segment_avg_wait=("wait_time", "mean"),
            segment_avg_fare=("booking_value", "mean"),
            segment_avg_distance=("ride_distance", "mean"),
        )
        .reset_index()
    )
    df = df.merge(segment_stats, on=group_cols, how="left")

    city_stats = (
        df.groupby("city")
        .agg(
            city_bookings=("booking_status", "size"),
            city_avg_fare=("booking_value", "mean"),
        )
        .reset_index()
    )
    df = df.merge(city_stats, on="city", how="left")

    df["distance_bucket"] = pd.cut(
        df["ride_distance"],
        bins=[-0.1, 3, 8, 15, 10_000],
        labels=["short", "medium", "long", "very_long"],
    ).astype(str)
    df["fare_bucket"] = pd.qcut(
        df["booking_value"].rank(method="first"),
        q=4,
        labels=["low", "mid", "high", "premium"],
    ).astype(str)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Saved modeling dataset: {output_file} ({len(df):,} rows)")
    return df


if __name__ == "__main__":
    build_features()
