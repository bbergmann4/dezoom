#!/usr/bin/env python
# coding: utf-8


import pandas as pd
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
    if filename[-3:] == 'csv':
        print(f"begin loading simple csv file {filename}")
        df = pd.read_csv(url)
        df.to_sql(table, engine, if_exists='replace')
        print(f"Loaded file to table {table}")
    elif filename[-7:] == 'parquet':
        print(f"begin loading parquet file {filename}")
        df = pd.read_parquet(url)
        df.to_sql(table, engine, if_exists='replace')
        print(f"Loaded file to table {table}")
    else:
        print("File type not supported")

if __name__ == '__main__':
    ingest_data()

