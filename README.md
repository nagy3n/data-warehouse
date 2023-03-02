# Project: Data Modeling with Postgres

## Introduction

A startup called **Sparkify** wants to analyze the data they've been collecting on songs and user activity on their new
music streaming app.

The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't
have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as
a directory with JSON metadata on the songs in their app.

As a Data engineer assigned to this project, my role is to create a Postgres database with tables designed to optimize
queries on song play analysis.

## Datasets

1. **`Song Dataset`**: The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON
   format and contains metadata about a song and the artist of that song. The files are partitioned by the first three
   letters of each song's track ID. For example, here are file paths to two files in this dataset.
   > `s3://udacity-dend/song_data/A/B/C/TRABCEI128F424C983.json`

   And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.
   > `{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}`


2. **`Log Dataset`**: The second dataset consists of log files in JSON format generated by this event simulator based on
   the songs in the dataset above. These simulate activity logs from a music streaming app based on specified
   configurations. For example, here are filepaths to two files in this dataset.
   > `s3://udacity-dend/log_data/2018/11/2018-11-12-events.json`

   And below is an example of what the data in a log file, 2018-11-12-events.json, looks like.
   > {"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}

## Running the python scripts

1. Before running the queries make sure you have created the redshift cluster, and associated with an
   IAM role which has read access on s3
2. Fill in dwh.cfg with the cluster details and IAM role name
3. Complete the **sql_queries.py** which has all the queries related to create, insert data, and drop table.
4. Open the terminal and run `python create_tables.py` command to drop and create tables. This command resets the database each time it is executed.
5. **etl.py**: Run `python etl.py` on terminal to copy the data from s3 to the staging tables and to insert the processed data in the star schema tables.

## Files in the Datasets

1. **song_data**: Contains data related to songs. This dataset is used to populate **staging_songs** table
2. **log_data**: Contains logs for song plays. This dataset is used to populate **staging_events** table

## Fact and Dimension Tables

1. **songplay**: This is the Fact table that takes all fields from staging_events table.
2. **user**: This is one of the dimension table that takes all fields from staging_events table
3. **song**: This is one of the dimension table that takes all fields from staging_songs table
4. **artist**: This is one of the dimension table that takes all fields from staging_songs table
5. **time**: This is one of the dimension table that takes all fields from staging_events table
