USE ride_hailing_intelligence;

SELECT
    l.city,
    l.location_name AS pickup_location,
    COUNT(*) AS bookings,
    SUM(f.is_cancelled) AS cancellations,
    ROUND(100 * AVG(f.is_cancelled), 2) AS cancellation_rate_pct,
    ROUND(AVG(f.wait_time), 2) AS avg_wait_time,
    ROUND(SUM(f.booking_value), 2) AS gross_booking_value
FROM fact_bookings f
JOIN dim_location l ON f.pickup_location_id = l.location_id
GROUP BY l.city, l.location_name
HAVING bookings >= 50
ORDER BY cancellation_rate_pct DESC, bookings DESC;

SELECT
    pickup.city,
    pickup.location_name AS pickup_location,
    dropoff.location_name AS drop_location,
    COUNT(*) AS bookings,
    ROUND(AVG(f.booking_value), 2) AS avg_booking_value,
    ROUND(100 * AVG(f.is_cancelled), 2) AS cancellation_rate_pct
FROM fact_bookings f
JOIN dim_location pickup ON f.pickup_location_id = pickup.location_id
JOIN dim_location dropoff ON f.drop_location_id = dropoff.location_id
GROUP BY pickup.city, pickup.location_name, dropoff.location_name
HAVING bookings >= 25
ORDER BY bookings DESC
LIMIT 30;
