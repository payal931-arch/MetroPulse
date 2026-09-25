-- MetroPulse
-- Weather demand mart
-- Grain: one row per weather condition bucket

CREATE OR REPLACE TABLE mart_weather_demand AS

SELECT
    CASE
        WHEN precipitation = 0 THEN 'No Rain'
        WHEN precipitation > 0 AND precipitation < 2.5 THEN 'Light Rain'
        WHEN precipitation >= 2.5 AND precipitation < 10 THEN 'Moderate Rain'
        ELSE 'Heavy Rain'
    END AS precipitation_category,

    COUNT(*) AS total_trips,

    SUM(passenger_count) AS total_passengers,

    SUM(total_amount) AS total_revenue,

    AVG(total_amount) AS avg_amount_per_trip,

    AVG(trip_distance) AS avg_trip_distance,

    MEDIAN(trip_duration_minutes) AS median_trip_duration_minutes,

    AVG(trip_duration_minutes) AS avg_trip_duration_minutes,

    AVG(temperature_2m) AS avg_temperature,

    AVG(relative_humidity_2m) AS avg_humidity,

    AVG(wind_speed_10m) AS avg_wind_speed,

    AVG(precipitation) AS avg_precipitation

FROM fact_taxi_trips

GROUP BY
    CASE
        WHEN precipitation = 0 THEN 'No Rain'
        WHEN precipitation > 0 AND precipitation < 2.5 THEN 'Light Rain'
        WHEN precipitation >= 2.5 AND precipitation < 10 THEN 'Moderate Rain'
        ELSE 'Heavy Rain'
    END

ORDER BY
    total_trips DESC;