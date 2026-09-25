\# MetroPulse Metric Dictionary



\## 1. Total Trips

\- Formula: COUNT(\*)

\- Grain: Individual taxi trip

\- Filters: Valid pickup/dropoff timestamps and valid core numeric fields

\- Exclusions: Invalid timestamp order, negative fare/total amount

\- Limitation: Represents recorded trips, not necessarily completed service demand.



\## 2. Total Passengers

\- Formula: SUM(passenger\_count)

\- Grain: Trip

\- Filters: Same as core taxi fact table

\- Limitation: Passenger count is a reported field and may contain missing or estimated values.



\## 3. Total Revenue

\- Formula: SUM(total\_amount)

\- Grain: Trip or selected aggregation

\- Filters: Valid taxi trips

\- Limitation: Total charged amount is used as the analytical revenue proxy.



\## 4. Average Amount per Trip

\- Formula: AVG(total\_amount)

\- Grain: Trip

\- Filters: Valid taxi trips

\- Limitation: Mean can be influenced by extreme values.



\## 5. Median Trip Amount

\- Formula: MEDIAN(total\_amount)

\- Grain: Trip

\- Filters: Valid taxi trips

\- Limitation: Describes the middle observation and does not represent total revenue.



\## 6. Average Trip Distance

\- Formula: AVG(trip\_distance)

\- Grain: Trip

\- Filters: Non-negative trip distance

\- Limitation: Based on recorded taxi trip distance.



\## 7. Trip Duration

\- Formula: dropoff\_datetime - pickup\_datetime

\- Grain: Trip

\- Filters: Dropoff must occur after pickup

\- Limitation: Long-duration trips may include unusual operational cases.



\## 8. Average Speed

\- Formula: trip\_distance / (trip\_duration\_minutes / 60)

\- Grain: Trip

\- Filters: Positive distance and duration

\- Limitation: Calculated average speed is not equivalent to road-segment traffic speed.



\## 9. Tip-to-Fare Percentage

\- Formula: SUM(tip\_amount) / SUM(fare\_amount) × 100

\- Grain: Selected payment group or aggregation

\- Filters: Fare amount must be non-zero

\- Limitation: Payment-type behavior can affect observed tipping patterns.



\## 10. Peak-Hour Share

\- Formula: Trips from 17:00–20:00 / all trips × 100

\- Grain: Full analysis period

\- Filters: Pickup hour between 17 and 20

\- Limitation: Peak window is defined for this analysis and may not represent every operational definition of peak.



\## 11. Rain-Hour Demand

\- Formula: Average hourly taxi trips during precipitation > 0

\- Grain: Date + hour

\- Filters: Precipitation greater than zero

\- Limitation: Observational association; does not establish that rain causes higher demand.



\## 12. Subway Ridership

\- Formula: SUM(ridership)

\- Grain: Hourly transit observation

\- Filters: Valid transit timestamp and ridership

\- Limitation: Aggregated subway ridership is compared with taxi demand at hourly level.



\## 13. Taxi–Subway Correlation

\- Formula: Pearson correlation between hourly taxi trips and subway ridership

\- Grain: Hour

\- Filters: Hours with available subway ridership

\- Limitation: Correlation does not establish causation.



\## 14. Anomaly Rate

\- Formula: Flagged trips / total trips × 100

\- Grain: Trip

\- Current thresholds:

&#x20; - Duration > 180 minutes

&#x20; - Distance > 100 miles

&#x20; - Total amount > $500

\- Limitation: Thresholds identify potential anomalies; they do not prove the records are incorrect.



\## 15. 95% Confidence Interval

\- Formula: Difference ± 1.96 × standard error

\- Grain: Comparison between two groups

\- Limitation: Interpretation depends on statistical assumptions and the observational nature of the data.

