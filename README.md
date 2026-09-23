\# MetroPulse



MetroPulse is an analytics project for a fictional urban mobility company

evaluating the New York City market.



The project combines NYC taxi trip data, weather data, taxi-zone information,

and subway ridership data to understand demand patterns, trip behaviour,

geographic opportunities, and factors associated with mobility demand.



\## Project Objective



The main objective is to build a reproducible analytics workflow that:



\- collects public data programmatically

\- preserves the raw data

\- cleans and validates the data

\- transforms the data using SQL

\- creates reusable analytical metrics

\- analyses demand across time and locations

\- studies relationships with weather and subway activity

\- presents the results through an interactive dashboard



\## Assessment Period



1 April 2024 to 30 June 2024



Core metrics will use the available records for the complete assessment

period. Sampling may only be used during development or exploratory work.



\## Data Sources



The project uses the following public sources:



1\. NYC TLC Yellow Taxi Trip Records

2\. NYC TLC Taxi Zone Lookup / Shapefile

3\. Open-Meteo Historical Weather API

4\. MTA Subway Hourly Ridership data



\## Technology



\- Python

\- Pandas

\- NumPy

\- DuckDB

\- SQL

\- PyArrow

\- SciPy

\- Plotly

\- Streamlit

\- Git / GitHub



\## Project Structure



```text

MetroPulse/

│

├── data/

│   ├── raw/

│   ├── staging/

│   └── processed/

│

├── src/

│   ├── ingestion/

│   ├── quality/

│   └── analysis/

│

├── sql/

│   ├── staging/

│   ├── intermediate/

│   └── marts/

│

├── tests/

├── dashboard/

├── docs/

│

├── .gitignore

├── requirements.txt

└── README.md

