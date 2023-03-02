import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS \"staging_events\";"
staging_songs_table_drop = "DROP TABLE IF EXISTS \"staging_songs\";"
songplay_table_drop = "DROP TABLE IF EXISTS \"songplay\";"
user_table_drop = "DROP TABLE IF EXISTS \"user\";"
song_table_drop = "DROP TABLE IF EXISTS \"song\";"
artist_table_drop = "DROP TABLE IF EXISTS \"artist\";"
time_table_drop = "DROP TABLE IF EXISTS \"time\";"

# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE "staging_events" (
    "artist" character varying(2048),
    "auth" character varying(2048),
    "firstName" character varying(2048),
    "gender" character varying(2048),
    "itemInSession" integer,
    "lastName" character varying(2048),
    "length" double precision,
    "level" character varying(2048),
    "location" character varying(2048),
    "method" character varying(2048),
    "page" character varying(2048),
    "registration" double precision,
    "sessionId" integer,
    "song" character varying(2048),
    "status" integer,
    "ts" bigint,
    "userAgent" character varying(2048),
    "userId" character varying(2048)
);
""")

staging_songs_table_create = ("""
CREATE TABLE "staging_songs" (
    "num_songs" integer NOT NULL,
    "artist_id" character varying(2048) NOT NULL,
    "artist_latitude" double precision,
    "artist_longitude" double precision,
    "artist_location" character varying(2048),
    "artist_name" character varying(2048),
    "song_id" character varying(2048),
    "title" character varying(2048),
    "duration" double precision,
    "year" integer
);
""")

songplay_table_create = ("""
CREATE TABLE "songplay" (
    "songplay_id" integer identity(0,1),
    "start_time" timestamp,
    "user_id" character varying(2048),
    "level" character varying(2048),
    "song_id" character varying(2048),
    "artist_id" character varying(2048),
    "session_id" integer,
    "location" character varying(2048),
    "user_agent" character varying(2048)
);
""")

user_table_create = ("""
CREATE TABLE "user" (
    "user_id" character varying(2048) PRIMARY KEY,
    "first_name" character varying(2048),
    "last_name" character varying(2048),
    "gender" character varying(2048),
    "level" character varying(2048)
);
""")

song_table_create = ("""
CREATE TABLE "song" (
    "song_id" character varying(2048) PRIMARY KEY,
    "title" character varying(2048),
    "artist_id" character varying(2048),
    "year" integer,
    "duration" double precision
);
""")

artist_table_create = ("""
CREATE TABLE "artist" (
    "artist_id" character varying(2048) PRIMARY KEY,
    "name" character varying(2048),
    "location" character varying(2048),
    "latitude" double precision,
    "longitude" double precision
);
""")

time_table_create = ("""
CREATE TABLE "time" (
    "start_time" timestamp PRIMARY KEY,
    "hour" integer,
    "day" integer,
    "week" integer,
    "month" integer,
    "year" integer,
    "weekday" integer
);
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {} credentials 'aws_iam_role={}' JSON {} region 'us-west-2';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    COPY staging_songs FROM {} credentials 'aws_iam_role={}' JSON 'auto' region 'us-west-2';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT
        TIMESTAMP 'epoch' + se.ts/1000 *INTERVAL '1 second',
        se.userId,
        se.level,
        se.song,
        se.artist,
        se.sessionId,
        se.location,
        se.userAgent
    FROM staging_events se
""")

user_table_insert = ("""
    INSERT INTO "user"(user_id, first_name, last_name, gender, level)
    SELECT 
        userId,
        firstName,
        lastName,
        gender,
        level
    FROM staging_events
""")

song_table_insert = ("""
    INSERT INTO song(song_id, title, artist_id, year, duration)
    SELECT 
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
""")

artist_table_insert = ("""
    INSERT INTO artist(artist_id, name, location, latitude, longitude)
    SELECT DISTINCT (artist_id)
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
""")

time_table_insert = ("""
    INSERT INTO time(start_time, hour, day, week, month, year, weekday)
    WITH temp_time AS (SELECT DISTINCT TIMESTAMP 'epoch' + (ts/1000 * INTERVAL '1 second') as ts FROM staging_events)
    SELECT ts,
        extract(hour from ts),
        extract(day from ts),
        extract(week from ts),
        extract(month from ts),
        extract(year from ts),
        extract(weekday from ts)
    FROM temp_time
""")

# QUERY LISTS

create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create
]
drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop
]
copy_table_queries = [
    staging_events_copy,
    staging_songs_copy
]
insert_table_queries = [
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert
]
