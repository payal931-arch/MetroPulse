CREATE OR REPLACE TABLE stg_mta AS
SELECT
    *
FROM read_json_auto(
    'data/raw/mta/mta_subway_2024-04_to_2024-06.json'
);