-- MetroPulse
-- Weather Impact Analysis

SELECT
    precipitation_category,
    total_trips,
    ROUND(
        100.0 * total_trips /
        (SELECT SUM(total_trips) FROM mart_weather_demand),
        2
    ) AS trip_share_pct,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(avg_amount_per_trip, 2) AS avg_amount_per_trip,
    ROUND(avg_trip_distance, 2) AS avg_trip_distance,
    ROUND(median_trip_duration_minutes, 2) AS median_trip_duration_minutes,
    ROUND(avg_temperature, 2) AS avg_temperature,
    ROUND(avg_precipitation, 2) AS avg_precipitation
FROM mart_weather_demand
ORDER BY total_trips DESC;