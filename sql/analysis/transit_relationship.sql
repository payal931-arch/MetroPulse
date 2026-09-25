-- MetroPulse
-- Taxi vs Subway Relationship Analysis

SELECT
    COUNT(*) AS hourly_observations,
    ROUND(
        CORR(taxi_trips, subway_ridership),
        4
    ) AS taxi_subway_correlation,
    ROUND(AVG(taxi_trips), 2) AS avg_taxi_trips,
    ROUND(AVG(subway_ridership), 2) AS avg_subway_ridership
FROM mart_transit_demand
WHERE subway_ridership IS NOT NULL;