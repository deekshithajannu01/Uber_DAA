# Data Dictionary

## fact_bookings

| Column | Meaning |
|---|---|
| `booking_id` | Unique booking identifier |
| `booking_datetime` | Booking timestamp |
| `city` | City of booking |
| `pickup_location` | Pickup area |
| `drop_location` | Drop area |
| `vehicle_type` | Auto, Bike, Mini, Sedan, SUV, etc. |
| `payment_method` | Payment type |
| `booking_status` | Raw booking status |
| `is_cancelled` | ML target: 1 if cancelled, 0 otherwise |
| `ride_distance` | Ride distance |
| `booking_value` | Booking/fare value |
| `driver_rating` | Driver rating |
| `customer_rating` | Customer rating |
| `wait_time` | Wait time before ride |
| `hour` | Booking hour |
| `day_of_week` | Day index |
| `is_weekend` | Weekend flag |
| `is_peak_hour` | Peak-hour flag |
| `fare_per_km` | Booking value divided by distance |
| `customer_cancel_reason` | Customer-side cancellation reason |
| `driver_cancel_reason` | Driver-side cancellation reason |

## Dashboard KPI Tables

| File | Use |
|---|---|
| `vehicle_cancellation_kpis.csv` | Vehicle-type cancellation comparison |
| `hourly_cancellation_kpis.csv` | Time-of-day cancellation behavior |
| `zone_cancellation_kpis.csv` | City and pickup-location risk |
| `feature_importance.csv` | ML explainability |
| `powerbi_model_summary.csv` | Best model and ROC-AUC |
| `powerbi_segment_risk.csv` | Segment-level risk table |
