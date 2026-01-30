## Question 1

On the _Metrics_ tab:

|Task|Name|Value|
|---|---|---|
|upload_to_gcs |file.size |134,481,400|


## Question 2

FROM 04_postgres_taxi

variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"

_renders to_

green_tipdata_2020-04.csv
  
## Question 3

Within bigquery:

SELECT
  count(unique_row_id) as numrows
FROM `triple-water-431925-m9.zoomcamp26.yellow_tripdata`

|numrows|
|---|
|24648219|

## Question 4

Within bigquery:


SELECT
  count(unique_row_id) as numrows
FROM
  `triple-water-431925-m9.zoomcamp26.green_tripdata`;

|numrows|
|---|
|1734051|

## Question 5

In Bigquery:

SELECT
  count(unique_row_id) as numrows
FROM
  triple-water-431925-m9.zoomcamp26.yellow_tripdata_2021_03

|numrows|
|---|
|1925152|

##Question 6

Kestra uses the TZ Identifier seen here:  https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
