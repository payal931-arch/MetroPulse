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

PAGE_SIZE = 50000
MAX_RETRIES = 3


def fetch_mta_data():
    print("Starting MTA subway data ingestion...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_data = []
    offset = 0

    while True:
        params = {
            "$limit": PAGE_SIZE,
            "$offset": offset,
            "$where": (
                f"transit_timestamp >= '{START_DATE}' "
                f"AND transit_timestamp <= '{END_DATE}'"
            ),
            "$order": "transit_timestamp ASC",
        }

        page_loaded = False

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(
                    f"Requesting rows {offset + 1} onward "
                    f"(attempt {attempt}/{MAX_RETRIES})..."
                )

                response = requests.get(
                    URL,
                    params=params,
                    timeout=60
                )

                response.raise_for_status()

                page = response.json()

                if not isinstance(page, list):
                    raise ValueError("MTA API returned an unexpected response format.")

                all_data.extend(page)

                print(f"Received {len(page)} rows.")

                page_loaded = True
                break

            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")

                if attempt < MAX_RETRIES:
                    time.sleep(2)
                else:
                    raise

        if not page_loaded:
            raise RuntimeError("Failed to load MTA data page.")

        if len(page) < PAGE_SIZE:
            break

        offset += PAGE_SIZE

    if not all_data:
        raise ValueError("MTA API returned no records.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

    metadata = {
        "source_url": URL,
        "source_period": "2024-04-01 to 2024-06-30",
        "extracted_at_utc": datetime.utcnow().isoformat(),
        "row_count": len(all_data),
        "page_size": PAGE_SIZE,
        "file": str(OUTPUT_FILE),
    }

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved MTA data: {OUTPUT_FILE}")
    print(f"Total rows: {len(all_data)}")
    print(f"Saved metadata: {METADATA_FILE}")
    print("MTA ingestion finished successfully.")


if __name__ == "__main__":
    fetch_mta_data()