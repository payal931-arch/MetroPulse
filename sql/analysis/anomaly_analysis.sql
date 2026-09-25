-- MetroPulse
-- Taxi Trip Anomaly Analysis

SELECT
    COUNT(*) AS total_trips,

    SUM(
        CASE
            WHEN trip_duration_minutes > 180 THEN 1
            ELSE 0
        END
    ) AS trips_over_3_hours,

    SUM(
        CASE
            WHEN trip_distance > 100 THEN 1
            ELSE 0
        END
    ) AS trips_over_100_miles,

    SUM(
        CASE
            WHEN total_amount > 500 THEN 1
            ELSE 0
        END
    ) AS trips_over_500_dollars,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN trip_duration_minutes > 180 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        4
    ) AS pct_over_3_hours,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN trip_distance > 100 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        4
    ) AS pct_over_100_miles,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN total_amount > 500 THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        4
    ) AS pct_over_500_dollars

FROM fact_taxi_trips;