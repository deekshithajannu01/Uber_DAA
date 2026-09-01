USE ride_hailing_intelligence;

SELECT
    customer_cancel_reason AS cancellation_reason,
    COUNT(*) AS cancellations
FROM fact_bookings
WHERE is_cancelled = TRUE
  AND customer_cancel_reason IS NOT NULL
  AND customer_cancel_reason <> ''
GROUP BY customer_cancel_reason
ORDER BY cancellations DESC;

SELECT
    driver_cancel_reason AS cancellation_reason,
    COUNT(*) AS cancellations
FROM fact_bookings
WHERE is_cancelled = TRUE
  AND driver_cancel_reason IS NOT NULL
  AND driver_cancel_reason <> ''
GROUP BY driver_cancel_reason
ORDER BY cancellations DESC;

SELECT
    is_peak_hour,
    COUNT(*) AS bookings,
    ROUND(100 * AVG(is_cancelled), 2) AS cancellation_rate_pct,
    ROUND(AVG(wait_time), 2) AS avg_wait_time
FROM fact_bookings
GROUP BY is_peak_hour;
