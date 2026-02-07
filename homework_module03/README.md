###Homework Module 3###

CREATE EXTERNAL TABLE triple-water-4319-m9.zoomcamp26.yellow2024_janjun 
OPTIONS (
  format = 'Parquet',
  uris = ['gs://de-zoombuck-4319/yellow_tripdata_2024*']
);


CREATE TABLE triple-water-4319-m9.zoomcamp26.yellow2024_janjun_table
AS SELECT * FROM triple-water-4319-m9.zoomcamp26.yellow2024_janjun; 

##Question 1##


SELECT count(VendorID) FROM triple-water-4319-m9.zoomcamp26.yellow2024_janjun;

|count|
|---|
|20332093|

##Question 2##

--External
SELECT count(DISTINCT PULocationID) FROM triple-water-4319-m9.zoomcamp26.yellow2024_janjun; 
-- This query will process 0 B when run.


--Internal
SELECT count(DISTINCT PULocationID) FROM triple-water-4319-m9.zoomcamp26.yellow2024_janjun_table;
-- This query will process 155.12 MB when run.

##Question 3##

SELECT count(DISTINCT PULocationID) as "PickUp Locations" FROM triple-water-4319-m9.zoomcamp26.yellow2024_janjun_table;

SELECT count(DISTINCT PULocationID) as "PickUp Locations", count(DISTINCT DOLocationID) as "DropOff Locations" FROM triple-water-4319-m9.zoomcamp26.yellow2024_janjun_table;

##Question 4##

SELECT count(VendorID) FROM triple-water-431915-m9.zoomcamp26.yellow2024_janjun_table
WHERE fare_amount = 0;

|count|
|---|
|8,333|

##Question 5##
CREATE TABLE triple-water-4319-m9.zoomcamp26.yellow2024_janjun_optimized
PARTITION BY
  TIMESTAMP_TRUNC(tpep_dropoff_datetime, DAY)
CLUSTER BY VendorID
AS SELECT * FROM triple-water-4319-m9.zoomcamp26.yellow2024_janjun;

##QUESTION 6##

-- Un-optimized Table
SELECT COUNT(DISTINCT VendorID)
FROM triple-water-431915-m9.zoomcamp26.yellow2024_janjun_table
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
--This query will process 310.24 MB when run.

--Optimized Table
SELECT COUNT(DISTINCT VendorID)
FROM  triple-water-431915-m9.zoomcamp26.yellow2024_janjun_optimized
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
--This query will process 26.84 MB when run.

##Question 7##

GCP Bucket

##Question 8##
False:  It may not make sense for smaller tables, especially if they are frequently updated.

##Question 9##

