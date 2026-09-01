USE ride_hailing_intelligence;

SELECT
    COUNT(*) AS total_bookings,
    SUM(is_cancelled) AS cancelled_bookings,
    ROUND(100 * AVG(is_cancelled), 2) AS cancellation_rate_pct,
    ROUND(SUM(booking_value), 2) AS gross_booking_value,
    ROUND(SUM(CASE WHEN is_cancelled THEN booking_value ELSE 0 END), 2) AS cancelled_booking_value
FROM fact_bookings;

SELECT
    v.vehicle_type,
    COUNT(*) AS bookings,
    SUM(f.is_cancelled) AS cancellations,
    ROUND(100 * AVG(f.is_cancelled), 2) AS cancellation_rate_pct,
    ROUND(AVG(f.booking_value), 2) AS avg_booking_value,
    ROUND(AVG(f.wait_time), 2) AS avg_wait_time
FROM fact_bookings f
JOIN dim_vehicle v ON f.vehicle_id = v.vehicle_id
GROUP BY v.vehicle_type
ORDER BY cancellation_rate_pct DESC;

SELECT
    hour_num,
    COUNT(*) AS bookings,
    ROUND(100 * AVG(is_cancelled), 2) AS cancellation_rate_pct,
    ROUND(AVG(wait_time), 2) AS avg_wait_time,
    ROUND(SUM(booking_value), 2) AS gross_booking_value
FROM fact_bookings
GROUP BY hour_num
ORDER BY hour_num;
