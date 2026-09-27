# MetroPulse Metric Dictionary

This document explains the main metrics used in the MetroPulse analysis, including how each metric is calculated, what level of data it uses, and any important limitations.

## 1. Total Trips

* **Formula:** COUNT(*)
* **Grain:** Individual taxi trip
* **Filters:** Valid pickup/dropoff timestamps and valid core numeric fields
* **Exclusions:** Invalid timestamp order, negative fare/total amount
* **Limitation:** This represents the trips recorded in the dataset. It may not be the same as total actual service demand.

## 2. Total Passengers

* **Formula:** SUM(passenger_count)
* **Grain:** Trip
* **Filters:** Same as the core taxi fact table
* **Limitation:** Passenger count is a reported field, so some records may have missing or estimated values.

## 3. Total Revenue

* **Formula:** SUM(total_amount)
* **Grain:** Trip or selected aggregation
* **Filters:** Valid taxi trips
* **Limitation:** Total charged amount is used as the revenue measure for this analysis.

## 4. Average Amount per Trip

* **Formula:** AVG(total_amount)
* **Grain:** Trip
* **Filters:** Valid taxi trips
* **Limitation:** The average can be affected by unusually high or low values.

## 5. Median Trip Amount

* **Formula:** MEDIAN(total_amount)
* **Grain:** Trip
* **Filters:** Valid taxi trips
* **Limitation:** The median represents the middle trip amount. It should not be used as a measure of total revenue.

## 6. Average Trip Distance

* **Formula:** AVG(trip_distance)
* **Grain:** Trip
* **Filters:** Non-negative trip distance
* **Limitation:** This is based on the trip distance recorded in the taxi data.

## 7. Trip Duration

* **Formula:** dropoff_datetime - pickup_datetime
* **Grain:** Trip
* **Filters:** Dropoff must occur after pickup
* **Limitation:** Very long trips may include unusual operational cases.

## 8. Average Speed

* **Formula:** trip_distance / (trip_duration_minutes / 60)
* **Grain:** Trip
* **Filters:** Positive distance and duration
* **Limitation:** This is the calculated average speed for a trip. It should not be treated as the actual traffic speed on individual roads.

## 9. Tip-to-Fare Percentage

* **Formula:** SUM(tip_amount) / SUM(fare_amount) × 100
* **Grain:** Selected payment group or aggregation
* **Filters:** Fare amount must be non-zero
* **Limitation:** Tipping patterns can vary depending on payment type and other factors.

## 10. Peak-Hour Share

* **Formula:** Trips from 17:00–20:00 / all trips × 100
* **Grain:** Full analysis period
* **Filters:** Pickup hour between 17 and 20
* **Limitation:** The 5 PM–8 PM window is the peak period used for this project. Other analyses may define peak hours differently.

## 11. Rain-Hour Demand

* **Formula:** Average hourly taxi trips during precipitation > 0
* **Grain:** Date + hour
* **Filters:** Precipitation greater than zero
* **Limitation:** This shows an observed relationship between rain and taxi demand. It does not prove that rain causes higher demand.

## 12. Subway Ridership

* **Formula:** SUM(ridership)
* **Grain:** Hourly transit observation
* **Filters:** Valid transit timestamp and ridership
* **Limitation:** Subway ridership is aggregated at the hourly level and is compared with taxi demand at the same hourly level.

## 13. Taxi–Subway Correlation

* **Formula:** Pearson correlation between hourly taxi trips and subway ridership
* **Grain:** Hour
* **Filters:** Hours with available subway ridership
* **Limitation:** Correlation shows how two variables move together. It does not prove that one causes a change in the other.

## 14. Anomaly Rate

* **Formula:** Flagged trips / total trips × 100
* **Grain:** Trip
* **Current thresholds:**

  * Duration > 180 minutes
  * Distance > 100 miles
  * Total amount > $500
* **Limitation:** These thresholds are used to flag potentially unusual records. A flagged record is not automatically an incorrect record.

## 15. 95% Confidence Interval

* **Formula:** Difference ± 1.96 × standard error
* **Grain:** Comparison between two groups
* **Limitation:** The interpretation depends on the statistical assumptions used and on the fact that this is observational data.
