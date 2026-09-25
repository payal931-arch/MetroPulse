-- MetroPulse
-- Zone dimension
-- Purpose: provide one unique record per taxi Location ID

CREATE OR REPLACE TABLE dim_zone AS

SELECT
    location_id,
    zone,
    borough,
    shape_geometry,
    shape_length,
    shape_area

FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY location_id
            ORDER BY shape_area DESC
        ) AS rn
    FROM stg_zones
)

WHERE rn = 1;