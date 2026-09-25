from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time

import requests


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "taxi"
RAW_DIR.mkdir(parents=True, exist_ok=True)

MONTHS = ["2024-04", "2024-05", "2024-06"]


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def download_taxi_file(month):
    file_name = f"yellow_tripdata_{month}.parquet"
    url = f"{BASE_URL}/{file_name}"
    output_path = RAW_DIR / file_name

    if output_path.exists():
        print(f"Already exists, skipping: {file_name}")
        return

    for attempt in range(1, 4):
        try:
            print(f"Downloading {file_name} (attempt {attempt}/3)...")

            response = requests.get(url, timeout=120)
            response.raise_for_status()

            temp_path = output_path.with_suffix(".part")
            temp_path.write_bytes(response.content)
            temp_path.replace(output_path)

            file_hash = calculate_sha256(output_path)

            metadata = {
                "source": "NYC TLC Yellow Taxi Trip Records",
                "source_url": url,
                "period": month,
                "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
                "file_name": file_name,
                "sha256": file_hash,
                "status": "downloaded",
            }

            metadata_path = output_path.with_suffix(".json")

            with open(metadata_path, "w", encoding="utf-8") as file:
                json.dump(metadata, file, indent=2)

            print(f"Saved: {output_path}")
            print(f"SHA256: {file_hash}")

            return

        except requests.RequestException as error:
            print(f"Download failed: {error}")

            if attempt < 3:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Could not download {file_name} after 3 attempts.")

        except Exception as error:
            print(f"Unexpected error while processing {file_name}: {error}")

            if attempt < 3:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Could not process {file_name} after 3 attempts.")


def main():
    print("Starting NYC TLC taxi data ingestion...")

    for month in MONTHS:
        download_taxi_file(month)

    print("Taxi ingestion finished.")


if __name__ == "__main__":
    main()