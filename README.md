# MetroPulse

MetroPulse is a data analysis project based on **NYC Yellow Taxi trips**. The main goal of the project is to understand taxi demand, fares, weather conditions, and subway activity in New York City.

For this project, I worked with data from **April 1, 2024 to June 30, 2024**. I combined taxi trip data with weather and subway information and used it to create analysis, data-quality checks, and an interactive dashboard.

## Live Dashboard

**MetroPulse Dashboard:**
https://metropulse-86pqfrlx6cjjuw27jnsfbe.streamlit.app/

The dashboard allows the analysis to be explored through different views instead of only looking at the raw data.

## What I Tried to Do

The main purpose of MetroPulse was to take raw transportation data and turn it into something that could be used for analysis and decision-making.

The overall flow of the project was:

**Raw Data → Staging → Cleaning/Transformation → Analytical Tables → Analysis → Dashboard**

I used this structure so that the data preparation and analysis steps could be repeated instead of doing everything manually.

The project also includes data-quality checks to identify problems such as invalid timestamps, negative fares, negative trip distances, and other unusual records.

## Analysis Period

**April 1, 2024 to June 30, 2024**

## Data Sources

### 1. NYC TLC Yellow Taxi Trip Records

The main dataset used in the project is the NYC Yellow Taxi trip data.

I used the monthly trip records for:

* April 2024
* May 2024
* June 2024

Source:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

This data was used for most of the taxi-related analysis, including trip volume, fares, distance, duration, and demand by hour and location.

### 2. NYC Taxi Zones

I also used NYC taxi-zone information to understand trips at the zone and borough level.

The taxi-zone data was taken from the official NYC Open Data platform.

Source:
https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/8meu-9t5y

The dataset contains information such as:

* Taxi-zone ID
* Borough
* Zone name
* Geographic information

The TLC shapefile endpoint was not accessible during the data collection process, so I used the available official NYC Open Data taxi-zone export instead.

### 3. Weather Data

For the weather part of the analysis, I used historical hourly weather data from Open-Meteo.

Source:
https://open-meteo.com/

The weather data includes:

* Temperature
* Precipitation
* Relative humidity
* Wind speed

I used the hourly data to compare taxi demand under different weather conditions. This is treated as an observational comparison, so the results should not be interpreted as proving that weather directly causes changes in taxi demand.

### 4. MTA Subway Ridership

Hourly subway ridership data was also included in the project.

Source:
https://data.ny.gov/

This data was used to compare subway activity with taxi demand during the same hours.

## Main Analysis

Some of the main things I looked at were:

* Total number of taxi trips
* Passenger count
* Total amount collected
* Average trip amount
* Median trip amount
* Average trip distance
* Trip duration
* Average speed
* Tip-to-fare percentage
* Peak-hour demand
* Taxi demand during rainy hours
* Subway ridership
* Relationship between taxi demand and subway ridership
* Unusual or potentially anomalous trips

The peak period used in the analysis was **5 PM to 8 PM**.

## Data Cleaning and Quality Checks

Before doing the analysis, I checked the data for some common problems.

For example, I checked for:

* Drop-off times that occurred before or at the pickup time
* Negative trip distances
* Negative fare amounts
* Negative total amounts
* Very long trips
* Very large distances
* Unusually high total amounts

These checks helped make sure that the analytical tables were based on reasonable records.

The project also keeps the data-quality checks separate so that the cleaning process can be tested instead of being assumed to be correct.

## Technology Used

The main tools and technologies used in this project are:

* **Python** – data processing and analysis
* **Pandas** – working with tabular data
* **DuckDB** – storing and querying the processed data
* **SQL** – data transformation and analysis
* **Requests** – downloading data from online sources
* **Streamlit** – building the interactive dashboard
* **Plotly** – creating charts and visualizations
* **Git / GitHub** – version control and project management

## Project Structure

The project follows a simple data pipeline:

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
Analytical Tables
   |
   +---- Analysis
   |
   +---- Data Quality Checks
   |
   v
Streamlit Dashboard
```

The idea was to keep the different stages separate so that the raw data, cleaned data, analysis, and dashboard were easier to manage.

## What the Analysis Showed

The analysis found that taxi demand was not evenly distributed throughout the day. The **5 PM to 8 PM** period accounted for a noticeable share of the trips.

Demand also varied between the three months in the analysis period. May had the highest monthly taxi demand among the three months.

The weather analysis showed that the average number of taxi trips per observed hour was higher during rainy hours than during non-rainy hours. However, this is an observed relationship and should not be treated as proof that rain itself caused the increase.

The zone-level analysis also showed differences in trip volume and revenue across different parts of New York City.

## Important Limitations

There are a few limitations to keep in mind when looking at the results.

First, the analysis is based on historical observational data. It can show patterns and relationships, but it does not prove cause and effect.

Taxi demand can also be affected by things that are not included in the available data, such as:

* Traffic
* Events
* Holidays
* Taxi availability
* Other external factors

Some unusual records were also reviewed through anomaly and sensitivity checks. Because of these limitations, the results should mainly be viewed as evidence that can help with planning and further testing rather than as guaranteed future results.

## Final Note

MetroPulse was built as an end-to-end data analytics project, starting with raw public data and ending with an interactive dashboard.

The main focus was not only on creating charts, but also on building a process that could be repeated: collecting the data, cleaning it, checking its quality, transforming it with SQL, performing the analysis, and finally presenting the results through the dashboard.
