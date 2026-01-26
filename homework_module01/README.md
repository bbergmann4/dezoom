

*QUESTION 1*


>$ docker run -it --entrypoint=bash python:3.13


#Run docker image for python3.13

>root@49fe2217fb78:/# python -V

#Python 3.13.11

>root@49fe2217fb78:/# pip -V

#pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

_The pip version is 25.3_

*QUESTION 2*
(See ingest_Data3.py for the upload process for this data)

>SELECT  EXTRACT(MONTH FROM lpep_pickup_datetime) as month
>, count(*) as trips
>FROM green_taxi_202511
>WHERE trip_distance <= 1.0
>GROUP BY 1

|"month"|"trips"|
|---|---|
|11|8007|
12|2|

_There were 8,007 trips in November_

*QUESTION 4*

-- This question could refer to the longest individual trip or the longest total miles driven.  

>SELECT 
>EXTRACT(DAY FROM lpep_pickup_datetime) as day
>,sum(trip_distance) as total_distance
>,max(trip_distance) as longest_ride
>FROM green_taxi_202511 WHERE trip_distance<100
>GROUP BY 1
>ORDER BY 3 desc
>LIMIT 1;

|"day"|"total_distance"|"longest_ride"|
|---|---|---|
|14|5594.690000000012|88.03|

_November 14 is the day with the longest ride_

*QUESTION 5*


>SELECT 	 "Zone"
>	,sum("total_amount")
>FROM green_taxi_202511 g
>LEFT JOIN taxi_zone_lookup z ON(g."PULocationID" = z."LocationID")
>GROUP BY 1
>ORDER BY 2 desc
>LIMIT 1

|"Zone"|"sum"|
|---|---|
|"East Harlem North"|257684.7000000002|

_The largest total earnings is from East Harlem North_

*QUESTION 6*

>SELECT 	 
>	pickup."Zone" as "PickUp_Zone"
>	,dropoff."Zone" as "DropOff_Zone"
>	,max(g."tip_amount") as "Largest Tip"
>FROM green_taxi_202511 g
>LEFT JOIN taxi_zone_lookup dropoff ON(g."DOLocationID" = dropoff."LocationID")
>LEFT JOIN taxi_zone_lookup pickup ON(g."PULocationID" = pickup."LocationID")
>WHERE  pickup."Zone"= 'East Harlem North'
>GROUP BY 1,2
>ORDER BY 3 desc


|"PickUp_Zone"|"DropOff_Zone"|"Largest Tip"|
|---|---|---|
|"East Harlem North"|"Yorkville West"|81.89|

_The best tip was on a trip to Yorkvill West_

*QUESTION 7*

https://developer.hashicorp.com/terraform/cli/commands/apply

_The the sequence is best described with the following:_
_terraform init, terraform apply -auto-approve, terraform destroy_