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

