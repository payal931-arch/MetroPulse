-- MetroPulse
-- Transit demand mart
-- Grain: one row per hour
-- Purpose: compare taxi demand with NYC subway ridership

CREATE OR REPLACE TABLE mart_transit_demand AS

WITH subway_hourly AS (

    SELECT
        date_trunc('hour', transit_timestamp) AS transit_hour,

        SUM(ridership) AS subway_ridership,

        SUM(transfers) AS subway_transfers,

        COUNT(DISTINCT station_complex_id) AS active_station_complexes

    FROM int_mta_clean

    GROUP BY
        date_trunc('hour', transit_timestamp)
)

SELECT
    h.trip_date,
    h.pickup_hour,

    h.total_trips AS taxi_trips,
    h.total_passengers AS taxi_passengers,
    h.total_revenue AS taxi_revenue,

    h.avg_amount_per_trip,
    h.avg_trip_distance,
    h.median_trip_duration_minutes,
    h.avg_speed_mph,

    s.subway_ridership,
    s.subway_transfers,
    s.active_station_complexes

FROM mart_hourly_demand AS h

LEFT JOIN subway_hourly AS s

    ON CAST(h.trip_date AS TIMESTAMP)
       + INTERVAL (h.pickup_hour) HOUR
       = s.transit_hour

ORDER BY
    h.trip_date,
    h.pickup_hour;