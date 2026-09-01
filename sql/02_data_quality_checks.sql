USE ride_hailing_intelligence;

SELECT
    COUNT(*) AS total_rows,
    SUM(booking_datetime IS NULL) AS missing_booking_datetime,
    SUM(booking_status IS NULL) AS missing_booking_status,
    SUM(ride_distance < 0) AS invalid_distance,
    SUM(booking_value < 0) AS invalid_booking_value,
    SUM(is_cancelled IS NULL) AS missing_cancel_target
FROM fact_bookings;

SELECT
    booking_status,
    COUNT(*) AS rows_count,
    ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS row_share_pct
FROM fact_bookings
GROUP BY booking_status
ORDER BY rows_count DESC;

SELECT
    MIN(booking_value) AS min_booking_value,
    MAX(booking_value) AS max_booking_value,
    AVG(booking_value) AS avg_booking_value,
    MIN(ride_distance) AS min_distance,
    MAX(ride_distance) AS max_distance,
    AVG(ride_distance) AS avg_distance
FROM fact_bookings;
