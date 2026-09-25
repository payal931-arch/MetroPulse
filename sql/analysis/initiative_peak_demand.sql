-- MetroPulse
-- Initiative Evidence: Peak-Hour Demand

WITH daily AS (
    SELECT
        CAST(pickup_datetime AS DATE) AS trip_date,
        COUNT(*) AS daily_trips
    FROM fact_taxi_trips
    GROUP BY CAST(pickup_datetime AS DATE)
),

peak AS (
    SELECT
        COUNT(*) AS peak_trips,
        COUNT(DISTINCT CAST(pickup_datetime AS DATE)) AS peak_days
    FROM fact_taxi_trips
    WHERE pickup_hour BETWEEN 17 AND 20
),

overall AS (
    SELECT COUNT(*) AS total_trips
    FROM fact_taxi_trips
)

SELECT
    peak.peak_trips,
    overall.total_trips,

    ROUND(
        100.0 * peak.peak_trips / overall.total_trips,
        2
    ) AS peak_share_pct,

    ROUND(
        1.0 * peak.peak_trips / peak.peak_days,
        0
    ) AS avg_peak_trips_per_day,

    ROUND(
        1.0 * overall.total_trips / peak.peak_days,
        0
    ) AS avg_total_trips_per_day

FROM peak, overall;