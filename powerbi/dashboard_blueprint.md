# Power BI Dashboard Blueprint

Build a four-page Power BI report using the CSV files generated in `reports/`.

## Data Tables To Import

Import these files:

- `reports/powerbi_fact_bookings.csv`
- `reports/powerbi_dim_date.csv`
- `reports/vehicle_cancellation_kpis.csv`
- `reports/hourly_cancellation_kpis.csv`
- `reports/zone_cancellation_kpis.csv`
- `reports/feature_importance.csv`
- `reports/powerbi_segment_risk.csv`
- `reports/powerbi_model_summary.csv`

## Relationships

Create this relationship:

- `fact_bookings[booking_datetime]` to `dim_date[date]` using a date-only column if you add one in Power BI.

Keep the KPI CSVs as standalone summary tables. They are already aggregated.

## Page 1: Executive Overview

Purpose: quick business health view.

Recommended visuals:

- Card: Total Bookings
- Card: Cancelled Bookings
- Card: Cancellation Rate
- Card: Gross Booking Value
- Card: Cancelled Booking Value
- Card: Average Wait Time
- Line chart: bookings by hour
- Column chart: cancellation rate by vehicle type
- Bar chart: top pickup locations by cancellation rate

Slicers:

- City
- Vehicle Type
- Payment Method
- Date

## Page 2: Cancellation Deep Dive

Purpose: explain why and where cancellations happen.

Recommended visuals:

- Matrix: city, pickup location, bookings, cancellations, cancellation rate, avg wait time
- Bar chart: cancellation rate by hour
- Bar chart: cancellation rate by vehicle type
- Donut chart: cancelled vs completed bookings
- Scatter chart: avg wait time vs cancellation rate by pickup location

Insight angle:

- Find high-booking and high-cancellation zones.
- Compare peak-hour and non-peak-hour cancellation behavior.

## Page 3: Location And Demand Intelligence

Purpose: operations planning.

Recommended visuals:

- Map or filled map: cancellation rate by city/location if geocoded
- Bar chart: gross booking value by pickup location
- Heatmap/matrix: hour vs city with bookings
- Table: high-risk pickup zones ranked by cancellation rate

Insight angle:

- Recommend driver repositioning in high-demand, high-cancellation zones.
- Identify pickup zones with long wait times.

## Page 4: ML Model Insights

Purpose: show predictive modeling credibility.

Recommended visuals:

- Card: Model ROC-AUC
- Card: Best Model
- Bar chart: top feature importance
- Image: `reports/figures/confusion_matrix.png`
- Table: segment risk from `powerbi_segment_risk.csv`

Insight angle:

- Explain which factors drive cancellation.
- Convert model output into business rules for prevention.

## Suggested Formatting

- Use `powerbi/theme.json`.
- Format Cancellation Rate as percentage.
- Format booking values as currency.
- Use red/orange for cancellation-heavy visuals.
- Sort risk tables by cancellation rate descending.

