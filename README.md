# MetroPulse

MetroPulse is an end-to-end urban mobility intelligence platform for analyzing NYC Yellow Taxi demand, fares, weather, and subway activity for April 1, 2024 through June 30, 2024.

## Project Objective

The project combines taxi trip data, NYC taxi-zone information, historical weather data, and MTA subway hourly ridership to produce reusable analytical datasets and an interactive dashboard.

The workflow is designed to be reproducible:

Raw Sources → Staging → Intermediate → Analytical Marts → Analysis → Dashboard

## Analysis Period

April 1, 2024 – June 30, 2024

## Data Sources

### NYC TLC Yellow Taxi Trip Records
Monthly Yellow Taxi trip records for:
- April 2024
- May 2024
- June 2024

Source:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

### NYC Taxi Zones

NYC Taxi Zone data was obtained from the official NYC Open Data platform.

Source:
https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/8meu-9t5y

The downloaded export contains taxi-zone identifiers, boroughs, zone names, and geometry-related fields.

### Open-Meteo Historical Weather

Hourly NYC weather data was collected for the complete analysis period.

Source:
https://open-meteo.com/

### MTA Subway Hourly Ridership

Hourly subway ridership data was collected programmatically for the analysis period.

Source:
https://data.ny.gov/

## Technology Stack

- Python
- DuckDB
- SQL
- Pandas
- Requests
- Streamlit
- Plotly
- Git / GitHub

## Project Structure

```text
MetroPulse/
│
├── dashboard/
│   ├── app.py
│   └── data/
│
├── data/
│   └── raw/
│
├── database/
│   └── metropulse.duckdb
│
├── metadata/
│   └── source_metadata.json
│
├── sql/
│   ├── staging/
│   ├── intermediate/
│   ├── marts/
│   └── analysis/
│
├── src/
│   ├── ingestion/
│   │   ├── taxi.py
│   │   ├── weather.py
│   │   └── mta.py
│   ├── metadata.py
│   ├── rebuild_database.py
│   └── export_dashboard_data.py
│
├── tests/
│   └── data_quality_tests.py
│
├── metric_dictionary.md
├── requirements.txt
├── .gitignore
└── README.md