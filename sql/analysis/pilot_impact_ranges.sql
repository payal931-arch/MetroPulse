-- MetroPulse
-- Pilot Impact Range
-- Conservative scenarios for peak-hour and rain-responsive planning

WITH peak AS (
    SELECT
        COUNT(*) AS peak_trips
    FROM fact_taxi_trips
    WHERE pickup_hour BETWEEN 17 AND 20
),

rain AS (
    SELECT
        COUNT(*) AS rain_trips
    FROM fact_taxi_trips
    WHERE precipitation > 0
)

SELECT
    peak.peak_trips,

    ROUND(peak.peak_trips * 0.02, 0) AS peak_2pct_volume,
    ROUND(peak.peak_trips * 0.05, 0) AS peak_5pct_volume,

    rain.rain_trips,

    ROUND(rain.rain_trips * 0.02, 0) AS rain_2pct_volume,
    ROUND(rain.rain_trips * 0.05, 0) AS rain_5pct_volume

FROM peak, rain;