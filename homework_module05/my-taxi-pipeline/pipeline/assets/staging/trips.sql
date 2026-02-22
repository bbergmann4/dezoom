/* @bruin

type: bq.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: VendorID
    type: INTEGER
  - name: pickup_datetime
    type: TIMESTAMP
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: TIMESTAMP
    checks:
      - name: not_null
  - name: passenger_count
    type: INTEGER
    checks:
      - name: non_negative
  - name: trip_distance
    type: FLOAT
    checks:
      - name: non_negative
  - name: RatecodeID
    type: INTEGER
  - name: store_and_fwd_flag
    type: STRING
  - name: PULocationID
    type: INTEGER
  - name: DOLocationID
    type: INTEGER
  - name: payment_type
    type: INTEGER
    checks:
      - name: not_null
  - name: payment_type_name
    type: STRING
  - name: fare_amount
    type: FLOAT
    checks:
      - name: non_negative
  - name: tip_amount
    type: FLOAT
    checks:
      - name: non_negative
  - name: total_amount
    type: FLOAT
    checks:
      - name: non_negative
  - name: taxi_type
    type: STRING
  - name: extracted_at
    type: TIMESTAMP

@bruin */

-- Staging query:
-- 1) parse/normalize timestamps
-- 2) filter to the run window (required for time_interval materialization)
-- 3) deduplicate via ROW_NUMBER keeping the most recently extracted record
-- 4) enrich with payment lookup
-- The template variables `{{ start_datetime }}` and `{{ end_datetime }}` are provided by Bruin

WITH raw AS (
  SELECT
    *,
    SAFE_CAST(tpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    SAFE_CAST(tpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime
  FROM ingestion.trips
  WHERE SAFE_CAST(tpep_pickup_datetime AS TIMESTAMP) >= TIMESTAMP('{{ start_datetime }}')
    AND SAFE_CAST(tpep_pickup_datetime AS TIMESTAMP) < TIMESTAMP('{{ end_datetime }}')
),

ranked AS (
  SELECT
    r.*,
    ROW_NUMBER() OVER (
      PARTITION BY
        COALESCE(CAST(VendorID AS STRING), ''),
        COALESCE(tpep_pickup_datetime, ''),
        COALESCE(tpep_dropoff_datetime, ''),
        COALESCE(CAST(passenger_count AS STRING), ''),
        COALESCE(CAST(trip_distance AS STRING), ''),
        COALESCE(CAST(PULocationID AS STRING), ''),
        COALESCE(CAST(DOLocationID AS STRING), ''),
        COALESCE(CAST(payment_type AS STRING), '')
      ORDER BY SAFE_CAST(extracted_at AS TIMESTAMP) DESC
    ) AS rn
  FROM raw r
),

cleaned AS (
  SELECT * EXCEPT(rn) FROM ranked WHERE rn = 1
)

SELECT
  VendorID,
  pickup_datetime,
  dropoff_datetime,
  passenger_count,
  trip_distance,
  RatecodeID,
  store_and_fwd_flag,
  PULocationID,
  DOLocationID,
  cleaned.payment_type,
  lookup.payment_type_name,
  fare_amount,
  extra,
  mta_tax,
  tip_amount,
  tolls_amount,
  total_amount,
  congestion_surcharge,
  airport_fee,
  taxi_type,
  SAFE_CAST(extracted_at AS TIMESTAMP) AS extracted_at
FROM cleaned
LEFT JOIN ingestion.payment_lookup AS lookup
  ON cleaned.payment_type = lookup.payment_type_id
;
