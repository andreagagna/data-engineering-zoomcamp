#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name_1 = params.table_name_1
    url_1 = params.url_1
    table_name_2 = params.table_name_2
    url_2 = params.url_2
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    csv_name_1 = 'output.csv.gz'
    csv_name_2 = 'output.csv'

    os.system(f"wget {url_1} -O {csv_name_1}")
    os.system(f"wget {url_2} -O {csv_name_2}")

    engine = create_engine(f'postgresql+psycopg://{user}:{password}@{host}:{port}/{db}')

    df1 = pd.read_csv(csv_name_1)

    df1.lpep_pickup_datetime = pd.to_datetime(df1.lpep_pickup_datetime)
    df1.lpep_dropoff_datetime = pd.to_datetime(df1.lpep_dropoff_datetime)

    df2 = pd.read_csv(csv_name_2)

    dfs = [df1, df2]
    tables = [table_name_1, table_name_2]

    for i, df in enumerate(dfs):
        df.head(n=0).to_sql(name=tables[i], con=engine, if_exists='replace')
        df.to_sql(name=tables[i], con=engine, if_exists='append')
        print(f"Finished ingesting table {i} into the postgres database")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name_1', required=True, help='name of the first table where we will write the results to')
    parser.add_argument('--table_name_2', required=True, help='name of the second table where we will write the results to')
    parser.add_argument('--url_1', required=True, help='url of the first csv file')
    parser.add_argument('--url_2', required=True, help='url of the second csv file')

    args = parser.parse_args()

    main(args)
