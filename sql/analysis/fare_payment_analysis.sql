-- MetroPulse
-- Fare, Payment and Tipping Analysis

SELECT
    payment_type,
    COUNT(*) AS total_trips,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(MEDIAN(fare_amount), 2) AS median_fare,
    ROUND(AVG(total_amount), 2) AS avg_total_amount,
    ROUND(MEDIAN(total_amount), 2) AS median_total_amount,
    ROUND(AVG(tip_amount), 2) AS avg_tip_amount,
    ROUND(
        100.0 * SUM(tip_amount) /
        NULLIF(SUM(fare_amount), 0),
        2
    ) AS overall_tip_to_fare_pct
FROM fact_taxi_trips
GROUP BY payment_type
ORDER BY total_trips DESC;