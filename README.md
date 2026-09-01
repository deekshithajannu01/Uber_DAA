# Ride-Hailing Cancellation & Demand Intelligence Platform

An end-to-end Uber/Ola/Rapido-style analytics and machine learning project for predicting ride cancellations and identifying operational patterns behind failed bookings.

The project is designed around a real ride-hailing business problem:

> Can we predict which bookings are likely to be cancelled, and identify the locations, hours, vehicle types, and operational conditions driving cancellations?

## Recommended Dataset

Use this Kaggle dataset:

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

## How To Run With Real Kaggle Data

Create environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Download the Kaggle CSV and place it in:

```text
data/raw/ola_uber_ride_bookings.csv
```

Run:

```bash
python3 run_all.py
```

Check ROC-AUC:

```bash
cat reports/model_metrics.json
```

## Demo Run Without Kaggle Data

If you want to test the pipeline before downloading the real dataset:

```bash
python3 sample_data.py
python3 run_all.py
```

Important: the sample dataset is synthetic and should only be used to test the code. Use the Kaggle dataset for your actual portfolio metrics.

## Generated Outputs

```text
data/processed/clean_ride_bookings.csv
data/processed/modeling_dataset.csv
reports/powerbi_fact_bookings.csv
reports/powerbi_dim_date.csv
reports/powerbi_segment_risk.csv
reports/powerbi_model_summary.csv
reports/executive_kpis.csv
reports/vehicle_cancellation_kpis.csv
reports/hourly_cancellation_kpis.csv
reports/zone_cancellation_kpis.csv
reports/model_metrics.json
reports/feature_importance.csv
reports/figures/confusion_matrix.png
reports/figures/feature_importance.png
models/cancellation_model.joblib
```

## Power BI Dashboard

The `powerbi/` folder contains a complete Power BI build kit:

- `dashboard_blueprint.md`: page-by-page dashboard layout
- `dax_measures.dax`: measures to paste into Power BI
- `power_query_import.m`: import script starter
- `theme.json`: report theme
- `data_dictionary.md`: field definitions

Run the pipeline first:

```bash
python3 run_all.py
```

Then import the generated files from `reports/` into Power BI Desktop.

## Portfolio Positioning

This project is stronger than a generic ride dashboard because it includes:

- real cancellation prediction
- ROC-AUC based model evaluation
- cancellation reason analytics
- vehicle-level operational insights
- city and pickup-zone risk analysis
- SQL warehouse design
- model scoring table for future deployment

## Possible Business Recommendations

Examples of final recommendations you can generate:

- reduce wait time in high-cancellation pickup zones
- assign better-rated drivers to high-risk bookings
- review vehicle availability during evening peak hours
- create driver incentives for cancellation-heavy zones
- flag high-value rides with elevated cancellation probability
- identify whether customer-side or driver-side cancellations dominate

## License

MIT License
