-- MetroPulse
-- Temporal Demand Analysis
-- Purpose: Analyze taxi demand by month, weekday and hour

-- 1. Demand by month
SELECT
    pickup_month AS month,
    COUNT(*) AS total_trips,
    SUM(passenger_count) AS total_passengers,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_amount_per_trip
FROM fact_taxi_trips
GROUP BY pickup_month
ORDER BY pickup_month;


-- 2. Demand by day of week
SELECT
    pickup_day_of_week,
    COUNT(*) AS total_trips,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_amount_per_trip
FROM fact_taxi_trips
GROUP BY pickup_day_of_week
ORDER BY pickup_day_of_week;


-- 3. Demand by hour
SELECT
    pickup_hour,
    COUNT(*) AS total_trips,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_amount_per_trip,
    MEDIAN(trip_duration_minutes) AS median_trip_duration_minutes
FROM fact_taxi_trips
GROUP BY pickup_hour
ORDER BY pickup_hour;


-- 4. Peak-hour share
WITH hourly AS (
    SELECT
        pickup_hour,
        COUNT(*) AS total_trips
    FROM fact_taxi_trips
    GROUP BY pickup_hour
),
peak AS (
    SELECT
        SUM(total_trips) AS peak_trips
    FROM hourly
    WHERE pickup_hour BETWEEN 17 AND 20
),
overall AS (
    SELECT COUNT(*) AS all_trips
    FROM fact_taxi_trips
)
SELECT
    peak.peak_trips,
    overall.all_trips,
    ROUND(
        100.0 * peak.peak_trips / overall.all_trips,
        2
    ) AS peak_hour_share_pct
FROM peak, overall;