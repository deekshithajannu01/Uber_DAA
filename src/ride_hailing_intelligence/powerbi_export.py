from __future__ import annotations

import json

import pandas as pd

from .config import CLEAN_FILE, FEATURE_FILE, REPORT_DIR


def export_powerbi_tables() -> None:
    """Create Power BI-friendly fact and dimension tables."""
    bookings = pd.read_csv(CLEAN_FILE, parse_dates=["booking_datetime"])
    modeling = pd.read_csv(FEATURE_FILE)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    fact_cols = [
        "booking_id",
        "booking_datetime",
        "city",
        "pickup_location",
        "drop_location",
        "vehicle_type",
        "payment_method",
        "booking_status",
        "is_cancelled",
        "ride_distance",
        "booking_value",
        "driver_rating",
        "customer_rating",
        "wait_time",
        "hour",
        "day_of_week",
        "is_weekend",
        "is_peak_hour",
        "fare_per_km",
        "customer_cancel_reason",
        "driver_cancel_reason",
    ]
    available_fact_cols = [col for col in fact_cols if col in bookings.columns]
    bookings[available_fact_cols].to_csv(REPORT_DIR / "powerbi_fact_bookings.csv", index=False)

    date_dim = (
        bookings[["booking_datetime"]]
        .dropna()
        .assign(date=lambda d: d["booking_datetime"].dt.date)
        .drop_duplicates("date")
        .sort_values("date")
    )
    date_dim["year"] = pd.to_datetime(date_dim["date"]).dt.year
    date_dim["month"] = pd.to_datetime(date_dim["date"]).dt.month
    date_dim["month_name"] = pd.to_datetime(date_dim["date"]).dt.month_name()
    date_dim["day"] = pd.to_datetime(date_dim["date"]).dt.day
    date_dim["day_name"] = pd.to_datetime(date_dim["date"]).dt.day_name()
    date_dim["is_weekend"] = pd.to_datetime(date_dim["date"]).dt.dayofweek.isin([5, 6]).astype(int)
    date_dim.drop(columns=["booking_datetime"]).to_csv(REPORT_DIR / "powerbi_dim_date.csv", index=False)

    for column, filename in [
        ("vehicle_type", "powerbi_dim_vehicle.csv"),
        ("payment_method", "powerbi_dim_payment.csv"),
        ("city", "powerbi_dim_city.csv"),
        ("pickup_location", "powerbi_dim_pickup_location.csv"),
    ]:
        if column in bookings.columns:
            bookings[[column]].drop_duplicates().sort_values(column).to_csv(REPORT_DIR / filename, index=False)

    if "distance_bucket" in modeling.columns:
        segment = (
            modeling.groupby(["city", "vehicle_type", "distance_bucket"], as_index=False)
            .agg(
                bookings=("booking_status", "size"),
                cancellation_rate=("is_cancelled", "mean"),
                avg_booking_value=("booking_value", "mean"),
                avg_wait_time=("wait_time", "mean"),
            )
            .sort_values("cancellation_rate", ascending=False)
        )
        segment.to_csv(REPORT_DIR / "powerbi_segment_risk.csv", index=False)

    metrics_path = REPORT_DIR / "model_metrics.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        summary = pd.DataFrame(
            [
                {
                    "best_model": metrics.get("best_model"),
                    "best_test_roc_auc": metrics.get("best_test_roc_auc"),
                }
            ]
        )
        summary.to_csv(REPORT_DIR / "powerbi_model_summary.csv", index=False)

    print(f"Exported Power BI tables to {REPORT_DIR}")


if __name__ == "__main__":
    export_powerbi_tables()
