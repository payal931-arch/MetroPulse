import requests
from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone


URL = "https://archive-api.open-meteo.com/v1/archive"

PARAMS = {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "start_date": "2024-04-01",
    "end_date": "2024-06-30",
    "hourly": "temperature_2m,precipitation,relative_humidity_2m,wind_speed_10m",
    "timezone": "America/New_York",
}


OUTPUT_DIR = Path("data/raw/weather")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "nyc_weather_2024-04_to_2024-06.json"
META_FILE = OUTPUT_DIR / "nyc_weather_2024-04_to_2024-06_metadata.json"


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():
    print("Starting NYC weather data ingestion...")

    response = requests.get(URL, params=PARAMS, timeout=60)
    response.raise_for_status()

    data = response.json()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    file_hash = calculate_sha256(OUTPUT_FILE)

    metadata = {
        "source_url": URL,
        "source_period": "2024-04-01 to 2024-06-30",
        "extraction_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "latitude": PARAMS["latitude"],
        "longitude": PARAMS["longitude"],
        "timezone": PARAMS["timezone"],
        "sha256": file_hash,
    }

    with open(META_FILE, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    print(f"Saved weather data: {OUTPUT_FILE}")
    print(f"Saved metadata: {META_FILE}")
    print(f"SHA256: {file_hash}")
    print("Weather ingestion finished.")


if __name__ == "__main__":
    main()