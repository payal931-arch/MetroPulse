-- MetroPulse
-- Weather Comparison with Uncertainty
-- Compare No Rain vs Rain

WITH trip_groups AS (
    SELECT
        CASE
            WHEN precipitation = 0 THEN 'No Rain'
            ELSE 'Rain'
        END AS weather_group,
        total_amount
    FROM fact_taxi_trips
),

summary AS (
    SELECT
        weather_group,
        COUNT(*) AS trip_count,
        AVG(total_amount) AS mean_amount,
        STDDEV_SAMP(total_amount) AS std_amount
    FROM trip_groups
    GROUP BY weather_group
),

comparison AS (
    SELECT
        MAX(CASE WHEN weather_group = 'No Rain'
            THEN trip_count END) AS no_rain_trips,

        MAX(CASE WHEN weather_group = 'Rain'
            THEN trip_count END) AS rain_trips,

        MAX(CASE WHEN weather_group = 'No Rain'
            THEN mean_amount END) AS no_rain_mean,

        MAX(CASE WHEN weather_group = 'Rain'
            THEN mean_amount END) AS rain_mean,

        MAX(CASE WHEN weather_group = 'No Rain'
            THEN std_amount END) AS no_rain_std,

        MAX(CASE WHEN weather_group = 'Rain'
            THEN std_amount END) AS rain_std
    FROM summary
)

SELECT
    no_rain_trips,
    rain_trips,

    ROUND(no_rain_mean, 2) AS no_rain_mean_amount,
    ROUND(rain_mean, 2) AS rain_mean_amount,

    ROUND(rain_mean - no_rain_mean, 2) AS mean_amount_difference,

    ROUND(
        SQRT(
            POWER(no_rain_std, 2) / no_rain_trips
            +
            POWER(rain_std, 2) / rain_trips
        ),
        4
    ) AS standard_error,

    ROUND(
        (rain_mean - no_rain_mean)
        -
        1.96 * SQRT(
            POWER(no_rain_std, 2) / no_rain_trips
            +
            POWER(rain_std, 2) / rain_trips
        ),
        2
    ) AS ci_lower_95,

    ROUND(
        (rain_mean - no_rain_mean)
        +
        1.96 * SQRT(
            POWER(no_rain_std, 2) / no_rain_trips
            +
            POWER(rain_std, 2) / rain_trips
        ),
        2
    ) AS ci_upper_95

FROM comparison;