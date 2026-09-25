-- MetroPulse
-- Staging model for NYC Taxi Zones
-- Purpose: standardize taxi zone reference data

CREATE OR REPLACE TABLE stg_zones AS

SELECT
    CAST("Location ID" AS INTEGER) AS location_id,
    "Zone" AS zone,
    "Borough" AS borough,
    "Shape Geometry" AS shape_geometry,
    "Shape Length" AS shape_length,
    "Shape Area" AS shape_area

FROM read_csv_auto(
    'data/raw/zones/taxi_zone_lookup.csv',
    HEADER = TRUE
);