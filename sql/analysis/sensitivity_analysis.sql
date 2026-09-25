-- MetroPulse
-- Sensitivity Analysis
-- Compare core metrics before and after removing extreme trips

WITH base AS (
    SELECT
        COUNT(*) AS trips,
        AVG(total_amount) AS avg_amount,
        MEDIAN(total_amount) AS median_amount
    FROM fact_taxi_trips
),

filtered AS (
    SELECT
        COUNT(*) AS trips,
        AVG(total_amount) AS avg_amount,
        MEDIAN(total_amount) AS median_amount
    FROM fact_taxi_trips
    WHERE
        trip_duration_minutes <= 180
        AND trip_distance <= 100
        AND total_amount <= 500
)

SELECT
    base.trips AS base_trips,
    filtered.trips AS filtered_trips,

    ROUND(base.avg_amount, 2) AS base_avg_amount,
    ROUND(filtered.avg_amount, 2) AS filtered_avg_amount,

    ROUND(base.median_amount, 2) AS base_median_amount,
    ROUND(filtered.median_amount, 2) AS filtered_median_amount,

    ROUND(
        100.0 * (filtered.avg_amount - base.avg_amount)
        / base.avg_amount,
        2
    ) AS avg_amount_change_pct,

    ROUND(
        100.0 * (filtered.median_amount - base.median_amount)
        / base.median_amount,
        2
    ) AS median_amount_change_pct

FROM base, filtered;