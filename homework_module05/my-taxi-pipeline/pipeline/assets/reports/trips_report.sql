/* @bruin

# Docs:
# - SQL assets: https://getbruin.com/docs/bruin/assets/sql
# - Materialization: https://getbruin.com/docs/bruin/assets/materialization
# - Quality checks: https://getbruin.com/docs/bruin/quality/available_checks

# TODO: Set the asset name (recommended: reports.trips_report).
name: report.trips_report

# TODO: Set platform type.
# Docs: https://getbruin.com/docs/bruin/assets/sql
# suggested type: duckdb.sql
type: bq.sql

# TODO: Declare dependency on the staging asset(s) this report reads from.
depends:
  - staging.trips

# TODO: Choose materialization strategy.
# For reports, `time_interval` is a good choice to rebuild only the relevant time window.
# Important: Use the same `incremental_key` as staging (e.g., pickup_datetime) for consistency.
materialization:
  type: table
  # suggested strategy: time_interval
  strategy: time_interval
  # TODO: set to your report's date column
  incremental_key: pickup_datetime
  # TODO: set to `date` or `timestamp`
  time_granularity: timestamp

# TODO: Define report columns + primary key(s) at your chosen level of aggregation.
columns:
  - name: Year
    type: INTEGER
    description: The year of the pickup datetime
  - name: Month
    type: INTEGER
    description: The month of the pickup datetime
  - name: fare_amount
    type: FLOAT
    description: The total fare amount for the group of trips
    checks:
      - name: non_negative
  - name: extra
    type: FLOAT
    description: The total extra amount for the group of trips
    checks:
      - name: non_negative
  - name: mta_tax
    type: FLOAT
    description: The total MTA tax for the group of trips
    checks:
      - name: non_negative
  - name: tip_amount
    type: FLOAT
    description: The total tip amount for the group of trips
    checks:
      - name: non_negative
  - name: tolls_amount
    type: FLOAT
    description: The total tolls amount for the group of trips
    checks:
      - name: non_negative
  - name: total_amount
    type: FLOAT
    description: The total amount for the group of trips
    checks:
      - name: non_negative
  - name: congestion_surcharge
    type: FLOAT
    description: The total congestion surcharge for the group of trips
    checks:
      - name: non_negative
  - name: airport_fee
    type: FLOAT
    description: The total airport fee for the group of trips
    checks:
      - name: non_negative
  - name: green_taxi_count  
    type: INTEGER
    description: The total number of green taxi trips in the group
    checks:
      - name: non_negative
  - name: yellow_taxi_count
    type: INTEGER
    description: The total number of yellow taxi trips in the group
    checks:
      - name: non_negative
  - name: total_trips
    type: INTEGER
    description: The total number of trips in the group
    checks:
      - name: non_negative  

@bruin */

-- Purpose of reports:
-- - Aggregate staging data for dashboards and analytics
-- Required Bruin concepts:
-- - Filter using `{{ start_datetime }}` / `{{ end_datetime }}` for incremental runs
-- - GROUP BY your dimension + date columns

SELECT 
  extract(year from pickup_datetime) AS year,
  extract(month from pickup_datetime) AS month,
  sum(fare_amount) AS fare_amount,
  sum(extra) AS extra,
  sum(mta_tax) AS mta_tax,
  sum(tip_amount) AS tip_amount,
  sum(tolls_amount) AS tolls_amount,
  sum(total_amount) AS total_amount,
  sum(congestion_surcharge) AS congestion_surcharge,
  sum(airport_fee) AS airport_fee,
  sum(case when taxi_type = 'green' then 1 else 0 end) AS green_taxi_count,
  sum(case when taxi_type = 'yellow' then 1 else 0 end) AS yellow_taxi_count,
  sum(1) AS total_trips
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
