-- ============================================================
-- MetroPulse Dashboard Filter Marts
-- ============================================================

-- ------------------------------------------------------------
-- 1. Drop-off zone performance
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE mart_dropoff_performance AS
SELECT
    dropoff_location_id,
    dropoff_zone,
    dropoff_borough,
    COUNT(*) AS total_trips,
    SUM(passenger_count) AS total_passengers,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes,
    MEDIAN(trip_duration_minutes) AS median_trip_duration_minutes,
    AVG(total_amount) AS avg_amount_per_trip
FROM fact_taxi_trips
GROUP BY
    dropoff_location_id,
    dropoff_zone,
    dropoff_borough;


-- ------------------------------------------------------------
-- 2. Rate code analysis
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE mart_rate_analysis AS
SELECT
    rate_code_id,
    COUNT(*) AS total_trips,
    SUM(passenger_count) AS total_passengers,
    SUM(fare_amount) AS total_fare_amount,
    SUM(total_amount) AS total_charged_amount,
    AVG(fare_amount) AS avg_fare_amount,
    AVG(total_amount) AS avg_amount_per_trip,
    MEDIAN(total_amount) AS median_amount
FROM fact_taxi_trips
GROUP BY
    rate_code_id;


-- ------------------------------------------------------------
-- 3. Airport trip analysis
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE mart_airport_analysis AS
SELECT
    CASE
        WHEN COALESCE(Airport_fee, 0) > 0
            THEN 'Airport Trip'
        ELSE 'Non-Airport Trip'
    END AS airport_flag,
    COUNT(*) AS total_trips,
    SUM(passenger_count) AS total_passengers,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_amount_per_trip,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM fact_taxi_trips
GROUP BY
    CASE
        WHEN COALESCE(Airport_fee, 0) > 0
            THEN 'Airport Trip'
        ELSE 'Non-Airport Trip'
    END;