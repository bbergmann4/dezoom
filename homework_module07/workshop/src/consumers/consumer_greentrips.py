import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kafka import KafkaConsumer
from greenmodels import ride_deserializer

server = 'localhost:9092'
topic_name = 'green-trips'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='rides-console02',
    value_deserializer=ride_deserializer
)

print(f"Listening to {topic_name}...")

long_rides_count = 0
counter = 0

for message in consumer:
    counter += 1
    ride = message.value
    if ride.trip_distance > 5.0:
        long_rides_count += 1
    print(f"Processed {counter} rides with {long_rides_count} having trip distance > 5.0")
        

consumer.close()
