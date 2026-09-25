-- MetroPulse
-- Monthly Comparison with Uncertainty
-- Compare April vs May 2024

WITH monthly AS (
    SELECT
        pickup_month,
        COUNT(*) AS trip_count,
        AVG(total_amount) AS mean_amount,
        STDDEV_SAMP(total_amount) AS std_amount
    FROM fact_taxi_trips
    WHERE pickup_month IN (4, 5)
    GROUP BY pickup_month
),

comparison AS (
    SELECT
        MAX(CASE WHEN pickup_month = 4 THEN trip_count END) AS april_trips,
        MAX(CASE WHEN pickup_month = 5 THEN trip_count END) AS may_trips,

        MAX(CASE WHEN pickup_month = 4 THEN mean_amount END) AS april_mean,
        MAX(CASE WHEN pickup_month = 5 THEN mean_amount END) AS may_mean,

        MAX(CASE WHEN pickup_month = 4 THEN std_amount END) AS april_std,
        MAX(CASE WHEN pickup_month = 5 THEN std_amount END) AS may_std
    FROM monthly
)

SELECT
    april_trips,
    may_trips,

    ROUND(
        100.0 * (may_trips - april_trips) / april_trips,
        2
    ) AS trip_change_pct,

    ROUND(april_mean, 2) AS april_mean_amount,
    ROUND(may_mean, 2) AS may_mean_amount,

    ROUND(may_mean - april_mean, 2) AS mean_amount_difference,

    ROUND(
        SQRT(
            POWER(april_std, 2) / april_trips
            +
            POWER(may_std, 2) / may_trips
        ),
        4
    ) AS standard_error,

    ROUND(
        (may_mean - april_mean)
        -
        1.96 * SQRT(
            POWER(april_std, 2) / april_trips
            +
            POWER(may_std, 2) / may_trips
        ),
        2
    ) AS ci_lower_95,

    ROUND(
        (may_mean - april_mean)
        +
        1.96 * SQRT(
            POWER(april_std, 2) / april_trips
            +
            POWER(may_std, 2) / may_trips
        ),
        2
    ) AS ci_upper_95

FROM comparison;