CREATE OR REPLACE TABLE mart_zone_opportunity AS
SELECT
    pickup_location_id,
    pickup_zone,
    pickup_borough,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount), 2) AS total_amount,
    ROUND(AVG(total_amount), 2) AS avg_amount_per_trip,
    ROUND(AVG(trip_distance), 2) AS avg_trip_distance,
    ROUND(AVG(trip_duration_minutes), 2) AS avg_trip_duration_minutes,
    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS trip_share_pct,
    CASE
        WHEN COUNT(*) < (
            SELECT AVG(zone_trips)
            FROM (
                SELECT COUNT(*) AS zone_trips
                FROM fact_taxi_trips
                GROUP BY pickup_location_id
            )
        )
        THEN 'Underserved'
        ELSE 'Higher Demand'
    END AS demand_indicator
FROM fact_taxi_trips
WHERE pickup_location_id IS NOT NULL
GROUP BY
    pickup_location_id,
    pickup_zone,
    pickup_borough;