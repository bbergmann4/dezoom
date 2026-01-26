#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import pyarrow.parquet as pq
from tqdm.auto import tqdm
from sqlalchemy import create_engine
import click




@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table', default='green_trip_202511', help='Target table name')
@click.option('--prefix', default='https://d37ci6vzurychx.cloudfront.net/trip-data/', help='URL excluding file nae')
@click.option('--filename', default='green_tripdata_2025-11.parquet', help='Name of .parquet file')

def ingest_data(user, password, host, port, db, table, prefix, filename):
    url = prefix+filename
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')


    first = True

    for chunk in tqdm(enumerate(read_parquet_in_chunks(url, batch_size = 10000))):

        if first:
            # Create table schema (no data)
            chunk.head(0).to_sql(
                name=table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        chunk.to_sql(
            name=table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))

        pass

def read_parquet_in_chunks(file_path, batch_size=1000):
    """
    Reads a Parquet file in chunks (batches) using pyarrow.
    """
    parquet_file = pq.ParquetFile(file_path)
    for record_batch in parquet_file.iter_batches(batch_size=batch_size):
        # Convert the RecordBatch to a pandas DataFrame
        df_chunk = record_batch.to_pandas()
        yield df_chunk

if __name__ == '__main__':
    ingest_data()

