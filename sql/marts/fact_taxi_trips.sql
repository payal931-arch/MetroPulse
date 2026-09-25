-- MetroPulse
-- Core taxi trip fact table
-- Grain: one cleaned taxi trip

CREATE OR REPLACE TABLE fact_taxi_trips AS

SELECT
    vendor_id,

    pickup_datetime,
    dropoff_datetime,

    pickup_year,
    pickup_month,
    pickup_day,
    pickup_hour,
    pickup_day_of_week,

    passenger_count,
    trip_distance,
    trip_duration_minutes,

    pickup_location_id,
    pickup_zone,
    pickup_borough,

    dropoff_location_id,
    dropoff_zone,
    dropoff_borough,

    rate_code_id,
    payment_type,

    fare_amount,
    tip_amount,
    tolls_amount,
    total_amount,
    congestion_surcharge,
    Airport_fee,

    temperature_2m,
    precipitation,
    relative_humidity_2m,
    wind_speed_10m

FROM int_taxi_weather;