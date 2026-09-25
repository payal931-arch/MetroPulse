-- MetroPulse
-- Initiative Evidence: Weather-Responsive Demand

WITH hourly AS (
    SELECT
        CAST(pickup_datetime AS DATE) AS trip_date,
        pickup_hour,

        CASE
            WHEN precipitation = 0 THEN 'No Rain'
            ELSE 'Rain'
        END AS weather_group,

        COUNT(*) AS taxi_trips

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
    ROUND(AVG(taxi_trips), 2) AS avg_trips_per_hour,
    ROUND(MEDIAN(taxi_trips), 2) AS median_trips_per_hour,
    ROUND(MIN(taxi_trips), 2) AS minimum_trips_per_hour,
    ROUND(MAX(taxi_trips), 2) AS maximum_trips_per_hour
FROM hourly
GROUP BY weather_group
ORDER BY weather_group;