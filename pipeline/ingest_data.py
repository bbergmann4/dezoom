#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click

prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
engine = create_engine('postgresql://root:root@localhost: 5432/ny_taxi')

dtype_v = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]



@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--month', default=1, type=int, help='Month of the data' )
@click.option('--year', default=2021, type=int, help='Year of the data' )

def ingest_data(user, password, host, port, db, table, month, year):
    url = f'{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')



    df_iter = pd.read_csv(
        url,
        dtype=dtype_v,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )


    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))

        pass

if __name__ == '__main__':
    ingest_data()











