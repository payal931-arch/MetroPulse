-- MetroPulse
-- Payment and tipping analysis mart
-- Grain: one row per payment type

CREATE OR REPLACE TABLE mart_payment_analysis AS

SELECT
    payment_type,

    COUNT(*) AS total_trips,

    SUM(passenger_count) AS total_passengers,

    SUM(fare_amount) AS total_fare_amount,

    SUM(tip_amount) AS total_tip_amount,

    SUM(total_amount) AS total_charged_amount,

    AVG(fare_amount) AS avg_fare_amount,

    AVG(total_amount) AS avg_amount_per_trip,

    AVG(tip_amount) AS avg_tip_amount,

    AVG(
        CASE
            WHEN fare_amount > 0
            THEN tip_amount / fare_amount
            ELSE NULL
        END
    ) AS avg_tip_rate,

    MEDIAN(total_amount) AS median_amount

FROM fact_taxi_trips

GROUP BY
    payment_type

ORDER BY
    total_trips DESC;