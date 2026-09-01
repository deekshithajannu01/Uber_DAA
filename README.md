# Ride-Hailing Cancellation & Demand Intelligence Platform

An end-to-end Uber/Ola/Rapido-style analytics and machine learning project for predicting ride cancellations and identifying operational patterns behind failed bookings.

The project is designed around a real ride-hailing business problem:

> Can we predict which bookings are likely to be cancelled, and identify the locations, hours, vehicle types, and operational conditions driving cancellations?

Used this Kaggle dataset:

**Ola & Uber: Ride Booking & Cancellation Data**  
https://www.kaggle.com/datasets/hetmengar/ola-and-uber-ride-booking-and-cancellation-data

Why this dataset is suitable:

- 100,000+ ride booking records
- Booking status / cancellation target
- Vehicle type information
- Cancellation patterns
- Useful for classification, SQL analytics, and business recommendations

Place the downloaded CSV inside:

```text
data/raw/
```

Recommended filename:

```text
data/raw/ola_uber_ride_bookings.csv
```

The pipeline also accepts common names like:

```text
ncr_ride_bookings.csv
ride_bookings.csv
bookings.csv
```

## Project Workflow

```text
Raw Ride Booking Dataset
        |
        v
Data Cleaning & Column Normalization
        |
        v
Cancellation Target Creation
        |
        v
Feature Engineering
        |
        +--> Cancellation Prediction Model
        |
        +--> Demand and Cancellation KPI Reports
        |
        v
SQL Warehouse + Business Analytics
        |
        v
Risk Segmentation & Recommendations
```

## Tech Stack

- Python: data cleaning, ML pipeline, reporting
- Pandas / NumPy: processing
- Scikit-learn: cancellation prediction
- MySQL / SQL: warehouse schema and analytics
- Matplotlib / Seaborn: charts
- Joblib: model persistence

## Machine Learning Problem

Target:

```text
is_cancelled = 1 if booking status contains cancelled
is_cancelled = 0 otherwise
```

Models trained:

- Logistic Regression
- Random Forest
- Histogram Gradient Boosting

Main metric:

```text
ROC-AUC
```

Additional metrics:

- PR-AUC
- classification report
- confusion matrix
- permutation feature importance

## Features

The model uses:

- city
- pickup location
- drop location
- vehicle type
- payment method
- ride distance
- booking value
- driver rating
- customer rating
- wait time
- hour
- day of week
- weekend flag
- peak-hour flag
- fare per km
- segment-level average wait/fare/distance

## SQL Analytics

The `sql/` directory contains:

| File | Purpose |
|---|---|
| `01_schema_ddl.sql` | Creates dimensional warehouse schema |
| `02_data_quality_checks.sql` | Validates ride booking data |
| `03_cancellation_kpis.sql` | Cancellation, vehicle, and hourly KPIs |
| `04_location_and_demand_analysis.sql` | Location and route-pair demand analysis |
| `05_cancellation_reason_analysis.sql` | Customer and driver cancellation reasons |
| `06_model_scoring_table.sql` | Table for storing model cancellation probabilities |

## Project Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── reports/
│   └── figures/
├── sql/
├── src/
│   └── ride_hailing_intelligence/
├── sample_data.py
├── run_all.py
├── requirements.txt
├── .gitignore
└── README.md
```

