
# Homework Module 4

## Question 1

int_trips_unioned only

## Question 2

dbt will fail the test, returning a non-zero exit code

## Question 3

My counts never came out exactly right (12459).  I think this is becuase a previous excercise  in Module 02 had us add 2021 yellow taxi data in as well.  I removed that  filename in my stg_yellow_tripdata.sql but I'm still getting slightly different counts.  I think the best troubleshooting would be to drop the table and rebuild, and I'll do that if I have time.  Until then, I'm choosing the closest value (12184).

```
SELECT count(revenue_month)
 FROM `triple-water-m9.dbt_bbergmann.fct_monthly_zone_revenue` 
  -- rows in table = 12459
  -- WHERE revenue_month < '2021-01-01' -- adding ceiling 12141
  -- AND revenue_month > '2018-12-01' -- floor and ceiling 11814
```


## Question 4
~~~
SELECT 
  service_type,
  pickup_zone,
  extract(YEAR FROM revenue_month), 
  sum(revenue_monthly_total_amount)
FROM `triple-water-m9.dbt_bbergmann.fct_monthly_zone_revenue` 
  WHERE revenue_month < '2021-01-01'
  AND revenue_month > '2019-12-01'
  AND service_type = 'Green'
GROUP BY 1 ,2, 3
ORDER BY 4 DESC
LIMIT 1
~~~
|service_type|pickup_zone|year|sum|
|---|---|---|---|
|Green	|East Harlem North	|2020|1817310.35|

## Question 5
~~~
SELECT 
  service_type,
  extract(YEAR FROM revenue_month), 
  extract(MONTH FROM revenue_month), 
  sum(total_monthly_trips)
FROM `triple-water-m9.dbt_bbergmann.fct_monthly_zone_revenue` 
  WHERE revenue_month < '2019-11-01'
  AND revenue_month > '2019-09-01'
  AND service_type = 'Green'
GROUP BY 1 ,2, 3
ORDER BY 4 DESC
LIMIT 1
~~~

|service_type|year|month|sum|
|---|---|---|---|
|Green	|2019	|10	|384624|

## Question 6
 
 Loaded FHV data
 - See update snippet to Kestra Task
 - See update to sources, staging/schema.yml
 - See new model:  stg_fhv_tripdata.sql

```
SELECT count(dispatch_base_id) FROM `triple-water--m9.dbt_bbergmann.stg_fhv_tripdata`

-- 43244693
```








