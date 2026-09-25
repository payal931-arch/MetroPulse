-- MetroPulse
-- Intermediate model for cleaned NYC Yellow Taxi trips
-- Purpose: validate trip timestamps, distance, duration and financial fields

CREATE OR REPLACE TABLE int_taxi_clean AS

SELECT
    VendorID AS vendor_id,
    tpep_pickup_datetime AS pickup_datetime,
    tpep_dropoff_datetime AS dropoff_datetime,
    passenger_count,
    trip_distance,
    RatecodeID AS rate_code_id,
    PULocationID AS pickup_location_id,
    DOLocationID AS dropoff_location_id,
    payment_type,
    fare_amount,
    tip_amount,
    tolls_amount,
    total_amount,
    congestion_surcharge,
    Airport_fee,

    date_diff(
        'minute',
        tpep_pickup_datetime,
        tpep_dropoff_datetime
    ) AS trip_duration_minutes,

    EXTRACT(YEAR FROM tpep_pickup_datetime) AS pickup_year,
    EXTRACT(MONTH FROM tpep_pickup_datetime) AS pickup_month,
    EXTRACT(DAY FROM tpep_pickup_datetime) AS pickup_day,
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
    DAYOFWEEK(tpep_pickup_datetime) AS pickup_day_of_week

FROM stg_taxi

WHERE
    tpep_pickup_datetime >= TIMESTAMP '2024-04-01 00:00:00'
    AND tpep_pickup_datetime < TIMESTAMP '2024-07-01 00:00:00'
    AND tpep_dropoff_datetime > tpep_pickup_datetime
    AND trip_distance >= 0
    AND fare_amount >= 0
    AND total_amount >= 0;