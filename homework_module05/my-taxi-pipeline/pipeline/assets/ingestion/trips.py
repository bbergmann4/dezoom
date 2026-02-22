"""@bruin

name: ingestion.trips
type: python
image: python:3.11
connection: GCP_Zoombox

materialization:
  type: table
  strategy: append

columns:
  - name: VendorID
    type: integer
    description: A code indicating the TPEP provider that provided the record
  - name: tpep_pickup_datetime
    type: string
    description: The date and time when the meter was engaged
  - name: tpep_dropoff_datetime
    type: string
    description: The date and time when the meter was disengaged
  - name: passenger_count
    type: integer
    description: The number of passengers in the vehicle
  - name: trip_distance
    type: float
    description: The elapsed trip distance in miles
  - name: RatecodeID
    type: integer
    description: The final rate code in effect at the end of the trip
  - name: store_and_fwd_flag
    type: string
    description: Whether the trip record was held in vehicle memory before sending
  - name: PULocationID
    type: integer
    description: TLC Taxi Zone in which the trip began
  - name: DOLocationID
    type: integer
    description: TLC Taxi Zone in which the trip ended
  - name: payment_type
    type: integer
    description: A numeric code indicating how the passenger paid for the trip
  - name: fare_amount
    type: float
    description: The time-and-distance fare charged by the meter
  - name: extra
    type: float
    description: Miscellaneous extras and surcharges
  - name: mta_tax
    type: float
    description: MTA tax automatically triggered based on the metered rate
  - name: tip_amount
    type: float
    description: Tip amount for the trip
  - name: tolls_amount
    type: float
    description: Total amount of tolls paid in trip
  - name: total_amount
    type: float
    description: The total amount charged to passengers
  - name: congestion_surcharge
    type: float
    description: Total amount collected for New York State congestion surcharge
  - name: airport_fee
    type: float
    description: Fee for airport trips (if applicable)
  - name: taxi_type
    type: string
    description: Type of taxi (yellow or green)
  - name: extracted_at
    type: string
    description: Timestamp when data was extracted

@bruin"""


import os
import json
import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def materialize():
    """
    Fetch NYC taxi trip data from the TLC public API endpoint.
    
    - Reads BRUIN_START_DATE and BRUIN_END_DATE environment variables
    - Reads taxi_types from BRUIN_VARS
    - Fetches parquet files from TLC endpoint for each taxi type and month
    - Returns concatenated DataFrame with extracted_at timestamp
    """
    # Get date range from environment
    start_date_str = os.getenv('BRUIN_START_DATE')
    end_date_str = os.getenv('BRUIN_END_DATE')
    
    if not start_date_str or not end_date_str:
        raise ValueError("BRUIN_START_DATE and BRUIN_END_DATE must be set")
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    # Get taxi types from pipeline variables
    bruin_vars = os.getenv('BRUIN_VARS', '{}')
    vars_dict = json.loads(bruin_vars)
    taxi_types = vars_dict.get('taxi_types', ['yellow', 'green'])
    
    if isinstance(taxi_types, str):
        taxi_types = [taxi_types]
    
    # TLC endpoint base URL
    base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    
    # Generate list of files to fetch
    all_dfs = []
    current_date = start_date
    
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        
        for taxi_type in taxi_types:
            # Construct the file URL
            filename = f'{taxi_type}_tripdata_{year}-{month:02d}.parquet'
            file_url = f'{base_url}/{filename}'
            
            try:
                # Fetch the parquet file
                response = requests.get(file_url, timeout=30)
                response.raise_for_status()
                
                # Read parquet data
                df = pd.read_parquet(file_url)
                
                # Add taxi_type column for identification
                df['taxi_type'] = taxi_type
                
                all_dfs.append(df)
                print(f"Fetched {filename}: {len(df)} rows")
                
            except requests.exceptions.HTTPError as e:
                print(f"File not found or error: {filename} - {e.response.status_code}")
                continue
            except Exception as e:
                print(f"Error fetching {filename}: {str(e)}")
                continue
        
        # Move to next month
        current_date += relativedelta(months=1)
    
    if not all_dfs:
        raise ValueError(f"No data found for taxi types {taxi_types} in date range {start_date} to {end_date}")
    
    # Concatenate all DataFrames
    final_df = pd.concat(all_dfs, ignore_index=True)
    
    # Add extracted_at timestamp for lineage
    final_df['extracted_at'] = datetime.utcnow().isoformat()
    
    return final_df


