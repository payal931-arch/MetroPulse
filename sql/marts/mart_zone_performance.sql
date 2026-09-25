-- MetroPulse
-- Zone performance mart
-- Grain: one row per pickup zone

CREATE OR REPLACE TABLE mart_zone_performance AS

SELECT
    pickup_location_id AS location_id,
    pickup_zone AS zone,
    pickup_borough AS borough,

    COUNT(*) AS total_trips,

    SUM(passenger_count) AS total_passengers,

    SUM(total_amount) AS total_revenue,

    SUM(trip_distance) AS total_distance,

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
    ) AS avg_speed_mph,

    AVG(
        CASE
            WHEN total_amount > 0
            THEN tip_amount / total_amount
            ELSE NULL
        END
    ) AS avg_tip_rate

FROM fact_taxi_trips

GROUP BY
    pickup_location_id,
    pickup_zone,
    pickup_borough

ORDER BY
    total_trips DESC;