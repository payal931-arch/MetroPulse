-- MetroPulse
-- Intermediate model for taxi trips with weather information
-- Purpose: attach hourly weather conditions to each taxi trip

CREATE OR REPLACE TABLE int_taxi_weather AS

SELECT
    t.*,

    w.temperature_2m,
    w.precipitation,
    w.relative_humidity_2m,
    w.wind_speed_10m

FROM int_taxi_zones AS t

LEFT JOIN stg_weather AS w
    ON DATE_TRUNC('hour', t.pickup_datetime)
       = CAST(w.weather_timestamp AS TIMESTAMP);