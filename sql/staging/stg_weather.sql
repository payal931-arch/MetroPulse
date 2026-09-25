-- MetroPulse
-- Staging model for NYC hourly weather data
-- Purpose: flatten Open-Meteo hourly arrays into one row per hour

CREATE OR REPLACE TABLE stg_weather AS

SELECT
    hourly.time[i] AS weather_timestamp,
    hourly.temperature_2m[i] AS temperature_2m,
    hourly.precipitation[i] AS precipitation,
    hourly.relative_humidity_2m[i] AS relative_humidity_2m,
    hourly.wind_speed_10m[i] AS wind_speed_10m

FROM read_json_auto(
    'data/raw/weather/nyc_weather_2024-04_to_2024-06.json'
),
UNNEST(
    generate_series(
        1,
        array_length(hourly.time)
    )
) AS t(i);