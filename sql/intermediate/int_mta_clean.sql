-- MetroPulse
-- Intermediate model for cleaned MTA subway ridership
-- Purpose: standardize timestamps and numeric transit measures

CREATE OR REPLACE TABLE int_mta_clean AS

SELECT
    CAST(transit_timestamp AS TIMESTAMP) AS transit_timestamp,

    transit_mode,
    station_complex_id,
    station_complex,
    borough,
    payment_method,
    fare_class_category,

    CAST(ridership AS DOUBLE) AS ridership,
    CAST(transfers AS DOUBLE) AS transfers,

    CAST(latitude AS DOUBLE) AS latitude,
    CAST(longitude AS DOUBLE) AS longitude

FROM stg_mta

WHERE
    transit_timestamp IS NOT NULL
    AND ridership IS NOT NULL;