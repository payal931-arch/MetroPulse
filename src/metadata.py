import os
import json
import hashlib
from datetime import datetime, timezone
import duckdb


# ============================================================
# CONFIGURATION
# ============================================================

DB_PATH = "database/metropulse.duckdb"
OUTPUT_PATH = "metadata/source_metadata.json"

ANALYSIS_PERIOD = {
    "start": "2024-04-01",
    "end": "2024-06-30"
}

SOURCE_INFO = {
    "taxi": {
        "url": "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
        "period": "April-June 2024"
    },
    "weather": {
        "url": "https://open-meteo.com/",
        "period": "2024-04-01 to 2024-06-30"
    },
    "mta": {
        "url": "https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-2020-2024/py8k-q2t6/about_data",
        "period": "2024-04-01 to 2024-06-30"
    },
    "zones": {
        "url": "https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/8meu-9t5y/about_data",
        "period": "NYC Taxi Zone reference data"
    }
}


# ============================================================
# HELPERS
# ============================================================

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def get_file_metadata(file_path):
    stat = os.stat(file_path)

    return {
        "file": file_path.replace("\\", "/"),
        "size_bytes": stat.st_size,
        "sha256": calculate_sha256(file_path)
    }


def get_schema_fingerprint(connection, query):
    columns = connection.execute(
        f"DESCRIBE SELECT * FROM ({query})"
    ).fetchall()

    schema = [
        {
            "column": row[0],
            "type": row[1]
        }
        for row in columns
    ]

    schema_string = json.dumps(
        schema,
        sort_keys=True
    )

    fingerprint = hashlib.sha256(
        schema_string.encode("utf-8")
    ).hexdigest()

    return schema, fingerprint


# ============================================================
# MAIN
# ============================================================

os.makedirs("metadata", exist_ok=True)

connection = duckdb.connect(DB_PATH)

metadata = {
    "project": "MetroPulse",
    "analysis_period": ANALYSIS_PERIOD,
    "metadata_generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "sources": []
}


# ============================================================
# TAXI
# ============================================================

taxi_files = []

for filename in sorted(
    os.listdir("data/raw/taxi")
):
    if filename.endswith(".parquet"):
        taxi_files.append(
            os.path.join(
                "data/raw/taxi",
                filename
            )
        )

for file_path in taxi_files:

    row_count = connection.execute(
        f"SELECT COUNT(*) FROM read_parquet('{file_path}')"
    ).fetchone()[0]

    query = f"SELECT * FROM read_parquet('{file_path}')"

    schema, fingerprint = get_schema_fingerprint(
        connection,
        query
    )

    file_info = get_file_metadata(file_path)

    metadata["sources"].append({
        "source_name": "NYC TLC Yellow Taxi",
        "source_url": SOURCE_INFO["taxi"]["url"],
        "source_period": SOURCE_INFO["taxi"]["period"],
        "extraction_timestamp_utc": metadata[
            "metadata_generated_at_utc"
        ],
        "row_count": row_count,
        "schema": schema,
        "schema_fingerprint": fingerprint,
        **file_info
    })


# ============================================================
# WEATHER
# ============================================================

weather_file = (
    "data/raw/weather/"
    "nyc_weather_2024-04_to_2024-06.json"
)

weather_count = connection.execute(
    f"""
    SELECT COUNT(*)
    FROM read_json_auto('{weather_file}')
    """
).fetchone()[0]

weather_query = (
    f"SELECT * FROM read_json_auto('{weather_file}')"
)

weather_schema, weather_fingerprint = get_schema_fingerprint(
    connection,
    weather_query
)

metadata["sources"].append({
    "source_name": "Open-Meteo Historical Weather",
    "source_url": SOURCE_INFO["weather"]["url"],
    "source_period": SOURCE_INFO["weather"]["period"],
    "extraction_timestamp_utc": metadata[
        "metadata_generated_at_utc"
    ],
    "row_count": weather_count,
    "schema": weather_schema,
    "schema_fingerprint": weather_fingerprint,
    **get_file_metadata(weather_file)
})


# ============================================================
# MTA
# ============================================================

mta_file = (
    "data/raw/mta/"
    "mta_subway_2024-04_to_2024-06.json"
)

mta_count = connection.execute(
    f"""
    SELECT COUNT(*)
    FROM read_json_auto('{mta_file}')
    """
).fetchone()[0]

mta_query = (
    f"SELECT * FROM read_json_auto('{mta_file}')"
)

mta_schema, mta_fingerprint = get_schema_fingerprint(
    connection,
    mta_query
)

metadata["sources"].append({
    "source_name": "MTA Subway Hourly Ridership",
    "source_url": SOURCE_INFO["mta"]["url"],
    "source_period": SOURCE_INFO["mta"]["period"],
    "extraction_timestamp_utc": metadata[
        "metadata_generated_at_utc"
    ],
    "row_count": mta_count,
    "schema": mta_schema,
    "schema_fingerprint": mta_fingerprint,
    **get_file_metadata(mta_file)
})


# ============================================================
# TAXI ZONES
# ============================================================

zones_file = (
    "data/raw/zones/taxi_zone_lookup.csv"
)

zones_count = connection.execute(
    f"""
    SELECT COUNT(*)
    FROM read_csv_auto(
        '{zones_file}',
        HEADER = TRUE
    )
    """
).fetchone()[0]

zones_query = f"""
    SELECT *
    FROM read_csv_auto(
        '{zones_file}',
        HEADER = TRUE
    )
"""

zones_schema, zones_fingerprint = get_schema_fingerprint(
    connection,
    zones_query
)

metadata["sources"].append({
    "source_name": "NYC Taxi Zones",
    "source_url": SOURCE_INFO["zones"]["url"],
    "source_period": SOURCE_INFO["zones"]["period"],
    "extraction_timestamp_utc": metadata[
        "metadata_generated_at_utc"
    ],
    "row_count": zones_count,
    "schema": zones_schema,
    "schema_fingerprint": zones_fingerprint,
    **get_file_metadata(zones_file)
})


# ============================================================
# WRITE METADATA
# ============================================================

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=2,
        default=str
    )


connection.close()

print("Source metadata generated successfully.")
print(f"Output: {OUTPUT_PATH}")
print(f"Sources recorded: {len(metadata['sources'])}")