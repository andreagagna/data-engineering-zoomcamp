## Question 1

- `--rm`

## Question 2

- 0.42.0

## Question 3

URL1=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
URL2=https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

docker run -it \
  --network=2_docker_sql_default \
  hw_ingest:v1 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name_1=green_taxi_trips \
    --url_1=${URL1} \
    --table_name_2=taxi_zones \
    --url_2=${URL2}

```SQL
SELECT
	COUNT(1)
FROM
	green_taxi_trips
WHERE
	DATE(lpep_pickup_datetime) = '2019-09-18' AND
	DATE(lpep_dropoff_datetime) = '2019-09-18';
```
Count = 15612

## Question 4

```SQL
SELECT
	DATE(lpep_pickup_datetime) AS date,
	*	
FROM
	green_taxi_trips
ORDER BY
	trip_distance DESC;
```
Date = 2019-09-26

# Question 5

```SQL
SELECT
	zones."Borough",
	SUM(trips.total_amount)
FROM
	green_taxi_trips trips
JOIN
	taxi_zones zones
ON
	trips."PULocationID" = zones."LocationID"
WHERE
	zones."Borough" != 'Unknown' AND
	DATE(trips.lpep_pickup_datetime) = '2019-09-18'
GROUP BY
	zones."Borough"
HAVING
	SUM(trips.total_amount) >= 50000
ORDER BY
	SUM(trips.total_amount) DESC;
```
"Brooklyn" "Manhattan" "Queens"

# Question 6

```SQL
SELECT
	trips.tip_amount,
	zones2."Zone" AS drop_off_zone,
	trips.*,
	zones1.*,
	zones2.*
FROM
	green_taxi_trips trips
JOIN
	taxi_zones zones1
ON
	trips."PULocationID" = zones1."LocationID"
JOIN
	taxi_zones zones2
ON
	trips."DOLocationID" = zones2."LocationID"
WHERE
	(TO_CHAR(trips.lpep_pickup_datetime, 'YYYY-MM') = '2019-09') AND
	(zones1."Zone" = 'Astoria')
ORDER BY
	trips.tip_amount DESC;
```
JFK Airport

# Question 8

```shell
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "EU"
      + max_time_travel_hours      = (known after apply)
      + project                    = "symbolic-bit-411809"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EU"
      + name                        = "symbolic-bit-411809-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 2s [id=projects/symbolic-bit-411809/datasets/demo_dataset]
google_storage_bucket.demo-bucket: Creation complete after 3s [id=symbolic-bit-411809-terra-bucket]
```