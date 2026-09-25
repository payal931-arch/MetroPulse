-- MetroPulse
-- Staging model for NYC Yellow Taxi trips
-- Purpose: standardize raw taxi fields before downstream transformations

CREATE OR REPLACE TABLE stg_taxi AS

SELECT
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    RatecodeID,
    store_and_fwd_flag,
    PULocationID,
    DOLocationID,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    Airport_fee

FROM read_parquet('data/raw/taxi/*.parquet')

WHERE tpep_pickup_datetime IS NOT NULL
  AND tpep_dropoff_datetime IS NOT NULL;