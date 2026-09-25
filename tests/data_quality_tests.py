import duckdb

DB_PATH = "database/metropulse.duckdb"

con = duckdb.connect(DB_PATH)

tests = []


def run_test(name, query, expected=True):
    try:
        result = con.execute(query).fetchone()[0]
        passed = result == expected

        tests.append({
            "test": name,
            "result": result,
            "expected": expected,
            "status": "PASS" if passed else "FAIL"
        })

    except Exception as e:
        tests.append({
            "test": name,
            "result": str(e),
            "expected": expected,
            "status": "ERROR"
        })


# 1. Clean taxi table should contain rows
run_test(
    "Clean taxi table is not empty",
    "SELECT COUNT(*) > 0 FROM int_taxi_clean"
)


# 2. Final fact table should contain rows
run_test(
    "Fact taxi table is not empty",
    "SELECT COUNT(*) > 0 FROM fact_taxi_trips"
)


# 3. Clean taxi row count should equal fact table row count
run_test(
    "Clean taxi and fact table row counts reconcile",
    """
    SELECT
        (SELECT COUNT(*) FROM int_taxi_clean)
        =
        (SELECT COUNT(*) FROM fact_taxi_trips)
    """
)


# 4. No invalid timestamp ordering
run_test(
    "No trips with dropoff before pickup",
    """
    SELECT COUNT(*) = 0
    FROM fact_taxi_trips
    WHERE dropoff_datetime <= pickup_datetime
    """
)


# 5. No negative trip distance
run_test(
    "No negative trip distance",
    """
    SELECT COUNT(*) = 0
    FROM fact_taxi_trips
    WHERE trip_distance < 0
    """
)


# 6. No negative fare amount
run_test(
    "No negative fare amount",
    """
    SELECT COUNT(*) = 0
    FROM fact_taxi_trips
    WHERE fare_amount < 0
    """
)


# 7. No negative total amount
run_test(
    "No negative total amount",
    """
    SELECT COUNT(*) = 0
    FROM fact_taxi_trips
    WHERE total_amount < 0
    """
)


# 8. No duplicate zone IDs
run_test(
    "Zone IDs are unique",
    """
    SELECT COUNT(*) = COUNT(DISTINCT location_id)
    FROM dim_zone
    """
)


# 9. Weather should cover all taxi hours
run_test(
    "All taxi trips have weather data",
    """
    SELECT COUNT(*) = 0
    FROM fact_taxi_trips
    WHERE temperature_2m IS NULL
    """
)


# 10. Transit mart should contain all taxi hours
run_test(
    "Transit mart has 2184 hourly records",
    """
    SELECT COUNT(*) = 2184
    FROM mart_transit_demand
    """
)


# Print results
print("\n========================================")
print("MetroPulse Data Quality Test Results")
print("========================================\n")

passed_count = 0

for test in tests:
    print(
        f"{test['status']:5} | "
        f"{test['test']} | "
        f"Result: {test['result']}"
    )

    if test["status"] == "PASS":
        passed_count += 1


print("\n========================================")
print(f"Passed: {passed_count}/{len(tests)}")
print("========================================")

con.close()