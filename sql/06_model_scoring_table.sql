CREATE TABLE IF NOT EXISTS model_cancellation_scores (
    booking_id VARCHAR(100),
    scored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancellation_probability DECIMAL(8,6),
    risk_band VARCHAR(20),
    PRIMARY KEY (booking_id, scored_at)
);

SELECT
    risk_band,
    COUNT(*) AS bookings,
    ROUND(AVG(cancellation_probability), 4) AS avg_cancel_probability
FROM model_cancellation_scores
GROUP BY risk_band
ORDER BY avg_cancel_probability DESC;
