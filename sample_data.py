from __future__ import annotations

import numpy as np
import pandas as pd

from src.ride_hailing_intelligence.config import SAMPLE_RAW_FILE


def generate_sample_data(rows: int = 25_000) -> None:
    rng = np.random.default_rng(42)
    cities = np.array(["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Pune"])
    vehicle_types = np.array(["Auto", "Bike", "Mini", "Prime Sedan", "SUV"])
    payment_methods = np.array(["UPI", "Cash", "Card", "Wallet"])
    pickup_zones = np.array(["Airport", "Railway Station", "Tech Park", "Mall", "Residential", "University", "Hospital", "Market"])
    cancel_reasons = np.array([
        "Driver not moving",
        "Customer changed plans",
        "Long wait time",
        "High fare",
        "Driver asked to cancel",
    ])

    booking_time = pd.date_range("2024-01-01", periods=rows, freq="20min")
    hour = booking_time.hour
    distance = rng.gamma(shape=2.2, scale=4.0, size=rows).clip(0.8, 45)
    wait_time = rng.gamma(shape=2.0, scale=3.2, size=rows).clip(1, 40)
    driver_rating = rng.normal(4.35, 0.35, rows).clip(2.5, 5.0)
    customer_rating = rng.normal(4.25, 0.45, rows).clip(2.0, 5.0)
    surge = ((hour >= 18) & (hour <= 21)) | ((hour >= 8) & (hour <= 10))
    fare = 45 + distance * rng.normal(17, 3, rows) + surge * rng.normal(35, 8, rows)

    pickup_choice = rng.choice(pickup_zones, rows)
    drop_choice = rng.choice(pickup_zones, rows)
    high_risk_zone = np.isin(pickup_choice, ["Airport", "Railway Station", "Tech Park"])
    cancel_logit = (
        -5.2
        + 0.18 * wait_time
        + 0.025 * fare
        + 0.90 * surge.astype(int)
        - 1.15 * (driver_rating - 4)
        - 0.55 * (customer_rating - 4)
        + 0.75 * (distance > 18)
        + 0.65 * high_risk_zone.astype(int)
    )
    cancel_prob = 1 / (1 + np.exp(-cancel_logit))
    cancelled = rng.binomial(1, cancel_prob.clip(0.03, 0.70))

    df = pd.DataFrame(
        {
            "Booking ID": np.arange(1, rows + 1),
            "Date": booking_time.date.astype(str),
            "Time": booking_time.time.astype(str),
            "City": rng.choice(cities, rows),
            "Pickup Location": pickup_choice,
            "Drop Location": drop_choice,
            "Vehicle Type": rng.choice(vehicle_types, rows, p=[0.24, 0.20, 0.28, 0.18, 0.10]),
            "Ride Distance": distance.round(2),
            "Booking Value": fare.round(2),
            "Driver Ratings": driver_rating.round(2),
            "Customer Rating": customer_rating.round(2),
            "Payment Method": rng.choice(payment_methods, rows),
            "Wait Time": wait_time.round(2),
            "Booking Status": np.where(cancelled == 1, "Cancelled", "Completed"),
            "Cancelled Rides by Customer": np.where(cancelled & (rng.random(rows) > 0.45), 1, 0),
            "Cancelled Rides by Driver": np.where(cancelled & (rng.random(rows) <= 0.45), 1, 0),
            "Reason for cancelling by Customer": np.where(cancelled == 1, rng.choice(cancel_reasons, rows), ""),
            "Reason for cancelling by Driver": np.where(cancelled == 1, rng.choice(cancel_reasons, rows), ""),
        }
    )

    SAMPLE_RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SAMPLE_RAW_FILE, index=False)
    print(f"Generated sample dataset: {SAMPLE_RAW_FILE}")


if __name__ == "__main__":
    generate_sample_data()
