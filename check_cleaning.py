import duckdb

con = duckdb.connect("database/metropulse.duckdb")

print("Raw rows:", con.execute("SELECT COUNT(*) FROM stg_taxi").fetchone()[0])
print("Clean rows:", con.execute("SELECT COUNT(*) FROM int_taxi_clean").fetchone()[0])

print(
    "Invalid timestamp order:",
    con.execute("""
        SELECT COUNT(*)
        FROM stg_taxi
        WHERE tpep_dropoff_datetime <= tpep_pickup_datetime
    """).fetchone()[0]
)

print(
    "Negative distance:",
    con.execute("""
        SELECT COUNT(*)
        FROM stg_taxi
        WHERE trip_distance < 0
    """).fetchone()[0]
)

print(
    "Negative fare:",
    con.execute("""
        SELECT COUNT(*)
        FROM stg_taxi
        WHERE fare_amount < 0
    """).fetchone()[0]
)

print(
    "Negative total:",
    con.execute("""
        SELECT COUNT(*)
        FROM stg_taxi
        WHERE total_amount < 0
    """).fetchone()[0]
)

con.close()