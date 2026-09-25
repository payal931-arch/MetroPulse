import duckdb
import os

DB_PATH = "database/metropulse.duckdb"
OUTPUT_DIR = "dashboard\data"

TABLES = [
    "mart_executive_summary",
    "mart_daily_demand",
    "mart_hourly_demand",
    "mart_zone_performance",
    "mart_payment_analysis",
    "mart_weather_demand",
    "mart_transit_demand",
    "mart_quality",
    "mart_zone_opportunity",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

con = duckdb.connect(DB_PATH)

for table in TABLES:
    output_file = os.path.join(OUTPUT_DIR, f"{table}.csv")

    con.execute(
        f"COPY {table} TO '{output_file}' (HEADER, DELIMITER ',')"
    )

    print(f"Exported: {table}")

con.close()

print()
print("Dashboard data export completed successfully.")