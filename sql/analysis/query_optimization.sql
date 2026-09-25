-- MetroPulse
-- Query Optimization
-- Optimization 1: Date filtering
-- Optimization 2: Zone filtering

-- Create indexes on frequently filtered/joined columns
CREATE INDEX IF NOT EXISTS idx_fact_pickup_datetime
ON fact_taxi_trips(pickup_datetime);

CREATE INDEX IF NOT EXISTS idx_fact_pickup_location
ON fact_taxi_trips(pickup_location_id);

-- Optimized query 1: daily demand for June
EXPLAIN ANALYZE
SELECT
    CAST(pickup_datetime AS DATE) AS trip_date,
    COUNT(*) AS total_trips,
    SUM(total_amount) AS total_revenue
FROM fact_taxi_trips
WHERE pickup_datetime >= TIMESTAMP '2024-06-01 00:00:00'
  AND pickup_datetime < TIMESTAMP '2024-07-01 00:00:00'
GROUP BY CAST(pickup_datetime AS DATE)
ORDER BY trip_date;

-- Optimized query 2: zone-level demand
EXPLAIN ANALYZE
SELECT
    pickup_location_id,
    pickup_zone,
    COUNT(*) AS total_trips,
    SUM(total_amount) AS total_revenue
FROM fact_taxi_trips
WHERE pickup_location_id IS NOT NULL
GROUP BY pickup_location_id, pickup_zone
ORDER BY total_trips DESC;