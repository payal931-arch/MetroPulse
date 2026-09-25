-- MetroPulse
-- Hourly taxi demand mart
-- Grain: one row per date and pickup hour

CREATE OR REPLACE TABLE mart_hourly_demand AS

SELECT
    CAST(pickup_datetime AS DATE) AS trip_date,
    pickup_hour,

    COUNT(*) AS total_trips,

    SUM(passenger_count) AS total_passengers,

    SUM(total_amount) AS total_revenue,

    AVG(total_amount) AS avg_amount_per_trip,

    AVG(trip_distance) AS avg_trip_distance,

    MEDIAN(trip_duration_minutes) AS median_trip_duration_minutes,

    AVG(
        CASE
            WHEN trip_distance > 0
            THEN trip_distance / (trip_duration_minutes / 60.0)
            ELSE NULL
        END
    ) AS avg_speed_mph

FROM fact_taxi_trips

GROUP BY
    CAST(pickup_datetime AS DATE),
    pickup_hour

ORDER BY
    trip_date,
    pickup_hour;