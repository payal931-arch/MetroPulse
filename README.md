# MetroPulse

MetroPulse is an end-to-end urban mobility intelligence platform for analyzing NYC Yellow Taxi demand, fares, weather, and subway activity for the period **April 1, 2024 through June 30, 2024**.

## Live Dashboard

[Open the MetroPulse Dashboard](https://metropulse-86pqfrlx6cjjuw27jnsfbe.streamlit.app/)

The project combines public transportation, taxi, weather, and geographic data to create a reproducible analytical pipeline and an interactive dashboard.

---

## Project Objective

The objective of MetroPulse is to transform raw urban mobility data into reusable analytical datasets and decision-support insights.

The workflow is:

**Raw Sources → Staging → Intermediate → Analytical Marts → Analysis → Dashboard**

The pipeline is designed to support reproducible ingestion, SQL-based transformations, data-quality validation, analysis, and dashboard reporting.

---

## Analysis Period

**April 1, 2024 through June 30, 2024**

---

## Data Sources

### NYC TLC Yellow Taxi Trip Records

Monthly NYC Yellow Taxi trip records were collected for:

- April 2024
- May 2024
- June 2024

Source:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

---

### NYC Taxi Zones

Taxi-zone information was obtained from the official NYC Open Data platform.

Source:

https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/8meu-9t5y

The dataset provides taxi-zone identifiers, boroughs, zone names, and geometry-related fields.

**Note:** The TLC shapefile endpoint was not accessible during ingestion, so the project uses the available official NYC Open Data taxi-zone export for zone attributes.

---

### Open-Meteo Historical Weather

Hourly NYC weather observations were collected for the complete analysis period.

Source:

https://open-meteo.com/

Weather variables include:

- Temperature
- Precipitation
- Relative humidity
- Wind speed

---

### MTA Subway Hourly Ridership

Hourly subway ridership data was collected programmatically for the analysis period.

Source:

https://data.ny.gov/

The dataset is used to analyze the relationship between subway activity and taxi demand.

---

## Technology Stack

- Python
- DuckDB
- SQL
- Pandas
- Requests
- Streamlit
- Plotly
- Git / GitHub

---

## Project Architecture

```text
Raw Data
   |
   v
Staging Tables
   |
   v
Intermediate Tables
   |
   v
Analytical Marts
   |
   +---- Analysis
   |
   +---- Data Quality
   |
   v
Streamlit Dashboard