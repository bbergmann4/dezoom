# Homework Module 07

## Setup


## Question 1:
$ docker exec -it workshop-redpanda-1 rpk version

```
rpk version: v25.3.9
Git ref:     836b4a36ef6d5121edbb1e68f0f673c2a8a244e2
Build date:  2026 Feb 26 07 48 21 Thu
OS/Arch:     linux/amd64
Go version:  go1.24.3
```

## Question 2:

- Rebuilt src/producers/producer.py to producer_greentrips.py
    - Change the url and columns
    - Changed the stream name
    - Removed the wait time
    - Imported new models module

- Rebuilt src/models.py to greenmodels.py
    - Changed the columns in the class and method
    - turned passenger count in to a float in order to handle NaN
    
uv run src/producers/producer_greentrips.py

``` took 7.91 seconds ```

## Question 3

- Rebuilt src/consumers/consumer.py to consumer_greentrips.py
    - Updated topic
    - Updated for loop to create counter

uv run src/consumers/consumer_greentrips.py

```
Processed 49416 rides with 8506 having trip distance > 5.0
```

## Question 4

 - Rebuilt src/job/aggregation_job.py to aggregation_job_greentrips.py
 - Created table in pgcli
 - A painful ammount of troubleshooting after the taskmanager crashed including updating available memory in flink-config.yaml

 ```
 postgres> select * from processed_events_aggregated order by num_trips desc limit 3
 ```

| window_start        | pulocationid | num_trips |
|---------------------|--------------|-----------|
| 2025-10-22 08:40:00 | 74           | 15        |
| 2025-10-20 16:30:00 | 74           | 14        |
| 2025-10-08 10:35:00 | 74           | 13        |


## Question 5 
 - Rebuilt previous script into session_job_greentrips.py

Got results nowhere near the available options.  I don't have a very good explanation for the discrepancy
 - Tried clearing stream and re-running
 - I get slightly different results on re-runs.  All outside of range.
 - Tried with a 1 minute session, but was also out of range.


```
postgres> select * from processed_events_session order by num_trips desc limit 3
```

| pulocationid | window_start        | window_end          | num_trips |
|--------------|---------------------|---------------------|-----------|
| 74           | 2025-10-29 07:07:37 | 2025-10-29 19:25:10 | 340       |
| 75           | 2025-10-29 07:07:37 | 2025-10-29 19:25:10 | 225       |
| 74           | 2025-10-28 06:50:13 | 2025-10-28 12:36:05 | 220       |

## Question 6
 - Rewrote aggregation job again as tipsum_job_greeentrips

```
postgres@localhost:postgres> select * from processed_events_tipsum  order by total_tips  desc limit 3

```

| window_start        | total_tips         |
|---------------------|--------------------|
| 2025-10-16 18:00:00 | 510.8599999999999  |
| 2025-10-30 16:00:00 | 494.41             |
| 2025-10-09 18:00:00 | 472.01000000000016 |
