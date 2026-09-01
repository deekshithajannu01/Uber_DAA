from __future__ import annotations

import pandas as pd

from .config import CLEAN_FILE, REPORT_DIR


def build_reports(input_file=CLEAN_FILE) -> dict[str, object]:
    df = pd.read_csv(input_file, parse_dates=["booking_datetime"])
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    executive = {
        "total_bookings": int(len(df)),
        "completed_bookings": int((df["is_cancelled"] == 0).sum()),
        "cancelled_bookings": int(df["is_cancelled"].sum()),
        "cancellation_rate": float(df["is_cancelled"].mean()),
        "gross_booking_value": float(df["booking_value"].sum()),
        "estimated_cancelled_value": float(df.loc[df["is_cancelled"] == 1, "booking_value"].sum()),
        "average_ride_distance": float(df["ride_distance"].mean()),
        "average_booking_value": float(df["booking_value"].mean()),
    }

    by_vehicle = (
        df.groupby("vehicle_type", as_index=False)
        .agg(
            bookings=("booking_status", "size"),
            cancellations=("is_cancelled", "sum"),
            cancellation_rate=("is_cancelled", "mean"),
            avg_booking_value=("booking_value", "mean"),
            avg_distance=("ride_distance", "mean"),
        )
        .sort_values("cancellation_rate", ascending=False)
    )

    by_hour = (
        df.groupby("hour", as_index=False)
        .agg(
            bookings=("booking_status", "size"),
            cancellation_rate=("is_cancelled", "mean"),
            gross_booking_value=("booking_value", "sum"),
            avg_wait_time=("wait_time", "mean"),
        )
        .sort_values("hour")
    )

    by_zone = (
        df.groupby(["city", "pickup_location"], as_index=False)
        .agg(
            bookings=("booking_status", "size"),
            cancellations=("is_cancelled", "sum"),
            cancellation_rate=("is_cancelled", "mean"),
            gross_booking_value=("booking_value", "sum"),
            avg_wait_time=("wait_time", "mean"),
        )
        .sort_values(["cancellation_rate", "bookings"], ascending=[False, False])
    )

    pd.Series(executive).to_csv(REPORT_DIR / "executive_kpis.csv", header=["value"])
    by_vehicle.to_csv(REPORT_DIR / "vehicle_cancellation_kpis.csv", index=False)
    by_hour.to_csv(REPORT_DIR / "hourly_cancellation_kpis.csv", index=False)
    by_zone.to_csv(REPORT_DIR / "zone_cancellation_kpis.csv", index=False)

    print(f"Saved analytics reports to {REPORT_DIR}")
    return executive


if __name__ == "__main__":
    build_reports()
