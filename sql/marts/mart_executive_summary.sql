-- MetroPulse
-- Executive Summary Mart
-- Grain: One row for the complete analysis period

CREATE OR REPLACE TABLE mart_executive_summary AS

WITH base AS (
    SELECT
        COUNT(*) AS total_trips,
        SUM(passenger_count) AS total_passengers,
        SUM(total_amount) AS total_revenue,
        AVG(total_amount) AS avg_amount_per_trip,
        MEDIAN(total_amount) AS median_amount_per_trip,
        AVG(trip_distance) AS avg_trip_distance,
        MEDIAN(trip_distance) AS median_trip_distance,
        MEDIAN(trip_duration_minutes) AS median_trip_duration_minutes,
        AVG(
            CASE
                WHEN trip_distance > 0
                THEN total_amount / trip_distance
                ELSE NULL
            END
        ) AS avg_amount_per_mile,
        AVG(
            CASE
                WHEN trip_duration_minutes > 0
                THEN total_amount / trip_duration_minutes
                ELSE NULL
            END
        ) AS avg_amount_per_minute
    FROM fact_taxi_trips
),

peak AS (
    SELECT
        COUNT(*) AS peak_trips
    FROM fact_taxi_trips
    WHERE pickup_hour BETWEEN 17 AND 20
),

airport AS (
    SELECT
        COUNT(*) AS airport_trips
    FROM fact_taxi_trips
    WHERE pickup_zone ILIKE '%Airport%'
       OR dropoff_zone ILIKE '%Airport%'
),

weather AS (
    SELECT
        COUNT(*) AS rainy_trips
    FROM fact_taxi_trips
    WHERE precipitation > 0
)

SELECT
    base.total_trips,
    base.total_passengers,
    ROUND(base.total_revenue, 2) AS total_revenue,
    ROUND(base.avg_amount_per_trip, 2) AS avg_amount_per_trip,
    ROUND(base.median_amount_per_trip, 2) AS median_amount_per_trip,
    ROUND(base.avg_trip_distance, 2) AS avg_trip_distance,
    ROUND(base.median_trip_distance, 2) AS median_trip_distance,
    ROUND(base.median_trip_duration_minutes, 2) AS median_trip_duration_minutes,
    ROUND(base.avg_amount_per_mile, 2) AS avg_amount_per_mile,
    ROUND(base.avg_amount_per_minute, 2) AS avg_amount_per_minute,

    peak.peak_trips,

    ROUND(
        100.0 * peak.peak_trips / base.total_trips,
        2
    ) AS peak_hour_share_pct,

    airport.airport_trips,

    ROUND(
        100.0 * airport.airport_trips / base.total_trips,
        2
    ) AS airport_trip_share_pct,

    weather.rainy_trips,

    ROUND(
        100.0 * weather.rainy_trips / base.total_trips,
        2
    ) AS rainy_trip_share_pct

FROM base
CROSS JOIN peak
CROSS JOIN airport
CROSS JOIN weather;