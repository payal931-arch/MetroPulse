-- MetroPulse
-- Contrarian Finding
-- Compare taxi demand during rain vs no-rain hours

WITH hourly_weather AS (
    SELECT
        CAST(pickup_datetime AS DATE) AS trip_date,
        pickup_hour,

        CASE
            WHEN precipitation = 0 THEN 'No Rain'
            ELSE 'Rain'
        END AS weather_group,

        COUNT(*) AS taxi_trips,
        AVG(total_amount) AS avg_amount,
        MEDIAN(trip_duration_minutes) AS median_duration

    FROM fact_taxi_trips
    GROUP BY
        CAST(pickup_datetime AS DATE),
        pickup_hour,
        CASE
            WHEN precipitation = 0 THEN 'No Rain'
            ELSE 'Rain'
        END
)

SELECT
    weather_group,
    COUNT(*) AS hourly_observations,
    SUM(taxi_trips) AS total_trips,
    ROUND(AVG(taxi_trips), 2) AS avg_trips_per_hour,
    ROUND(AVG(avg_amount), 2) AS avg_amount_per_trip,
    ROUND(AVG(median_duration), 2) AS avg_median_duration
FROM hourly_weather
GROUP BY weather_group
ORDER BY weather_group;