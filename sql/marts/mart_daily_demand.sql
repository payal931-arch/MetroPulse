-- MetroPulse
-- Daily taxi demand mart
-- Grain: one row per day

CREATE OR REPLACE TABLE mart_daily_demand AS

SELECT
    CAST(pickup_datetime AS DATE) AS trip_date,

    COUNT(*) AS total_trips,

    SUM(passenger_count) AS total_passengers,

    SUM(trip_distance) AS total_distance,

    SUM(total_amount) AS total_revenue,

    AVG(trip_distance) AS avg_trip_distance,

    AVG(trip_duration_minutes) AS avg_trip_duration_minutes,

    MEDIAN(trip_duration_minutes) AS median_trip_duration_minutes,

    AVG(total_amount) AS avg_amount_per_trip,

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
            THEN trip_distance / (trip_duration_minutes / 60.0)
            ELSE NULL
        END
    ) AS avg_speed_mph

FROM fact_taxi_trips

GROUP BY
    CAST(pickup_datetime AS DATE)

ORDER BY
    trip_date;