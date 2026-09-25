SELECT
    zone,
    borough,
    total_trips,
    ROUND(
        100.0 * total_trips /
        (SELECT SUM(total_trips) FROM mart_zone_performance),
        2
    ) AS trip_share_pct,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(
        100.0 * total_revenue /
        (SELECT SUM(total_revenue) FROM mart_zone_performance),
        2
    ) AS revenue_share_pct
FROM mart_zone_performance
ORDER BY total_trips DESC
LIMIT 15;