-- MetroPulse
-- Intermediate model for taxi trips with zone information
-- Purpose: enrich cleaned trips with pickup and drop-off zone attributes

CREATE OR REPLACE TABLE int_taxi_zones AS

SELECT
    t.*,

    p.zone AS pickup_zone,
    p.borough AS pickup_borough,

    d.zone AS dropoff_zone,
    d.borough AS dropoff_borough

FROM int_taxi_clean AS t

LEFT JOIN dim_zone AS p
    ON t.pickup_location_id = p.location_id

LEFT JOIN dim_zone AS d
    ON t.dropoff_location_id = d.location_id;