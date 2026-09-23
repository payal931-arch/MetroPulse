import csv
import json
import time
from datetime import datetime
from pathlib import Path

import requests


URL = "https://data.ny.gov/resource/wujg-7c2s.json"

START_DATE = "2024-04-01T00:00:00"
END_DATE = "2024-06-30T23:59:59"

OUTPUT_DIR = Path("data/raw/mta")
OUTPUT_FILE = OUTPUT_DIR / "mta_subway_2024-04_to_2024-06.json"
METADATA_FILE = OUTPUT_DIR / "mta_subway_2024-04_to_2024-06_metadata.json"


def fetch_mta_data():
    print("Starting MTA subway data ingestion...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    params = {
        "$limit": 50000,
        "$where": (
            f"transit_timestamp >= '{START_DATE}' "
            f"AND transit_timestamp <= '{END_DATE}'"
        ),
    }

    for attempt in range(1, 4):
        try:
            print(f"Querying MTA API (attempt {attempt}/3)...")

            response = requests.get(
                URL,
                params=params,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                raise ValueError("MTA API returned no records.")

            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            metadata = {
                "source_url": URL,
                "source_period": "2024-04-01 to 2024-06-30",
                "extracted_at_utc": datetime.utcnow().isoformat(),
                "row_count": len(data),
                "file": str(OUTPUT_FILE),
            }

            with open(METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            print(f"Saved MTA data: {OUTPUT_FILE}")
            print(f"Rows: {len(data)}")
            print(f"Saved metadata: {METADATA_FILE}")
            print("MTA ingestion finished.")

            return

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")

            if attempt < 3:
                time.sleep(2)
            else:
                raise


if __name__ == "__main__":
    fetch_mta_data()