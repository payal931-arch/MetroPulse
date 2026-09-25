import duckdb
import os

DB_PATH = "database/metropulse.duckdb"

SQL_FILES = [
    "sql/staging/stg_taxi.sql",
    "sql/staging/stg_weather.sql",
    "sql/staging/stg_mta.sql",
    "sql/staging/stg_zones.sql",

    "sql/intermediate/dim_zone.sql",
    "sql/intermediate/int_taxi_clean.sql",
    "sql/intermediate/int_taxi_zones.sql",
    "sql/intermediate/int_taxi_weather.sql",
    "sql/intermediate/int_mta_clean.sql",

    "sql/marts/fact_taxi_trips.sql",
    "sql/marts/mart_daily_demand.sql",
    "sql/marts/mart_zone_performance.sql",
    "sql/marts/mart_hourly_demand.sql",
    "sql/marts/mart_payment_analysis.sql",
    "sql/marts/mart_weather_demand.sql",
    "sql/marts/mart_transit_demand.sql",
    "sql/marts/mart_executive_summary.sql",
    "sql/marts/mart_quality.sql",
    "sql/marts/mart_zone_opportunity.sql",
]


def main():
    os.makedirs("database", exist_ok=True)

    con = duckdb.connect(DB_PATH)

    for sql_file in SQL_FILES:
        print(f"Running: {sql_file}")

        with open(sql_file, "r", encoding="utf-8") as file:
            sql = file.read()

        con.execute(sql)

    con.close()

    print()
    print("Database rebuild completed successfully.")


if __name__ == "__main__":
    main()