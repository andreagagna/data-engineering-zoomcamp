# Create an external table

```SQL
-- Create external table for Green Taxi 2022
CREATE OR REPLACE EXTERNAL TABLE `symbolic-bit-411809.ny_taxi.green_taxi_2022_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://mage-zoomcamp-andrea-gagna-3/nyc_taxi_data.parquet']
);
```

## Question 1

The tab details of BigQuery for the table of 2022 Green Taxi Data
counts 840,402 total records.

Otherwise, we can query
```SQL
SELECT COUNT(1)
FROM ``symbolic-bit-411809.ny_taxi.green_taxi_2022`;
```

## Question 2

```SQL
SELECT COUNT(DISTINCT(PULocationID))
FROM `symbolic-bit-411809.ny_taxi.green_taxi_2022`;
-- 6.41MB will be processed

SELECT COUNT(DISTINCT(PULocationID))
FROM `symbolic-bit-411809.ny_taxi.green_taxi_2022_external`;
-- 0MB will be processed
```

## Question 3

```SQL
SELECT COUNT(1)
FROM `symbolic-bit-411809.ny_taxi.green_taxi_2022`
WHERE fare_amount = 0;
```
There are 1,622 records with `fare_amount` of 0.


## Question 4

The best strategy for optimizing a table in BigQuery, given that your queries will always order the results by `PUlocationID` and filter based on `lpep_pickup_datetime`, is to:

- **Partition by `lpep_pickup_datetime` and Cluster on `PUlocationID`.**

Here's why this approach is optimal:

### Partitioning by `lpep_pickup_datetime`

Partitioning a table based on `lpep_pickup_datetime` is beneficial because it organizes data into segments,
each holding data for a specific range of time.
This setup is particularly useful for queries that filter on the `lpep_pickup_datetime` column,
as BigQuery can scan only the relevant partitions instead of the entire table. This results in faster query execution
and reduced costs since BigQuery charges based on the amount of data scanned.

### Clustering on `PUlocationID`

After partitioning by datetime, clustering by `PUlocationID` further organizes data within each partition.
Clustering sorts the data based on the `PUlocationID` values, making it faster to filter and sort by this column.
When a query filters by `lpep_pickup_datetime` (using partitioning) and then orders or filters by `PUlocationID` (using clustering),
BigQuery can quickly locate the relevant data within each partition, leading to even more efficient query execution.

### Why not the other options?

- **Cluster on `lpep_pickup_datetime` Partition by `PUlocationID`**: This is less optimal because `PUlocationID` likely
- has a wide range of values, making it a less efficient choice for partitioning compared to datetime.
- Datetime partitioning benefits time-based queries, which seem to be the primary filter based on your description.

- **Partition by `lpep_pickup_datetime` and Partition by `PUlocationID`**: BigQuery does not support partitioning
- a table on two different columns. You can only partition by one column and optionally cluster by up to four columns.

- **Cluster on by `lpep_pickup_datetime` and Cluster on `PUlocationID`**: Similar to the above, BigQuery does not support
- clustering a table without partitioning it first. Clustering is meant to be used in conjunction with partitioning
- to further organize the data within each partition.

Therefore, partitioning by `lpep_pickup_datetime` and clustering on `PUlocationID` is the most effective strategy
for optimizing your BigQuery table for the types of queries you intend to run. This approach leverages the strengths
of both partitioning and clustering to minimize query costs and improve performance.

-- Create a table partitioned by lpep_pickup_datetime
CREATE OR REPLACE TABLE `symbolic-bit-411809.ny_taxi.green_taxi_2022_partitioned`
PARTITION BY
  lpep_pickup_datetime AS
SELECT * FROM `symbolic-bit-411809.ny_taxi.green_taxi_2022`;
-- This query will process 120.52 MB when run


# Question 5

-- Query for materialized table
SELECT DISTINCT(PULocationID)
FROM `symbolic-bit-411809.ny_taxi.green_taxi_2022`
WHERE
  (lpep_pickup_datetime >= '2022-06-01') AND 
  (lpep_pickup_datetime <= '2022-06-30');
-- This query will process 12.82 MB when run

-- Query for partitioned table
SELECT DISTINCT(PULocationID)
FROM `symbolic-bit-411809.ny_taxi.green_taxi_2022_partitioned`
WHERE
  (lpep_pickup_datetime >= '2022-06-01') AND 
  (lpep_pickup_datetime <= '2022-06-30');
-- This query will process 1.12 MB when run


# Question 6

For an external table created in Google BigQuery, the data is stored in a Google Cloud Storage (GCP) Bucket.
External tables in BigQuery allow you to query data directly from files in Google Cloud Storage without loading
or moving the data into BigQuery storage. This means that the data remains in the GCP Bucket while BigQuery
can access and query the data directly from there.


# Question 7

False.

It is not always best practice to cluster your data in BigQuery.
While clustering can provide significant benefits in terms of query performance
and cost savings by organizing data based on the contents of one or more columns,
it is not universally applicable or beneficial for all datasets or use cases.

The decision to cluster a table should be based on factors such as the size of the dataset,
the query patterns (e.g., if you frequently filter or aggregate data based on the columns that you plan to cluster by),
and the specific performance and cost considerations of your BigQuery workloads.
Clustering may not provide benefits for small datasets or for tables where the query patterns do not align well with the clustered columns.


# Question 8

When you use SELECT COUNT(*) on a materialized table, BigQuery doesn't need to scan any data to count the rows;
instead, it can directly return the count of rows that has been previously computed and stored as part of the materialized table's metadata.