CREATE OR REPLACE TABLE mart_quality AS

SELECT
    CURRENT_TIMESTAMP AS generated_at,

    -- Raw vs clean reconciliation
    (SELECT COUNT(*) FROM stg_taxi) AS raw_taxi_rows,

    (SELECT COUNT(*) FROM int_taxi_clean) AS clean_taxi_rows,

    (SELECT COUNT(*) FROM fact_taxi_trips) AS fact_taxi_rows,

    -- Difference between clean and final fact table
    (
        SELECT COUNT(*) FROM int_taxi_clean
    )
    -
    (
        SELECT COUNT(*) FROM fact_taxi_trips
    ) AS clean_fact_difference,

    -- Timestamp quality
    (
        SELECT COUNT(*)
        FROM int_taxi_clean
        WHERE dropoff_datetime <= pickup_datetime
    ) AS invalid_timestamp_rows,

    -- Distance quality
    (
        SELECT COUNT(*)
        FROM int_taxi_clean
        WHERE trip_distance < 0
    ) AS negative_distance_rows,

    -- Fare quality
    (
        SELECT COUNT(*)
        FROM int_taxi_clean
        WHERE fare_amount < 0
    ) AS negative_fare_rows,

    -- Total amount quality
    (
        SELECT COUNT(*)
        FROM int_taxi_clean
        WHERE total_amount < 0
    ) AS negative_total_amount_rows,

    -- Weather matching
    (
        SELECT COUNT(*)
        FROM int_taxi_weather
        WHERE temperature_2m IS NULL
    ) AS missing_weather_rows,

    -- Zone matching
    (
        SELECT COUNT(*)
        FROM int_taxi_zones
        WHERE pickup_zone IS NULL
    ) AS missing_pickup_zone_rows,

    (
        SELECT COUNT(*)
        FROM int_taxi_zones
        WHERE dropoff_zone IS NULL
    ) AS missing_dropoff_zone_rows;