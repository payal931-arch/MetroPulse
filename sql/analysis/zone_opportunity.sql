SELECT
    zone,
    borough,
    total_trips,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(avg_amount_per_trip, 2) AS avg_amount_per_trip,
    ROUND(avg_speed_mph, 2) AS avg_speed_mph
FROM mart_zone_performance
WHERE total_trips >= 100000
ORDER BY avg_amount_per_trip ASC
LIMIT 15;