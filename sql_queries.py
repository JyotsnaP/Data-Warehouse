import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop  = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop       = "DROP TABLE IF EXISTS songplay;"
user_table_drop           = "DROP TABLE IF EXISTS users;"
song_table_drop           = "DROP TABLE IF EXISTS song;"
artist_table_drop         = "DROP TABLE IF EXISTS artist;"
time_table_drop           = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
staging_events_table_create= ("""
    CREATE TABLE staging_events
    (
        artist          VARCHAR,
        auth            VARCHAR,
        firstName       VARCHAR,
        gender          VARCHAR,
        itemInSession   INTEGER,
        lastName        VARCHAR,
        length          FLOAT,
        level           VARCHAR,
        location        VARCHAR,
        method          VARCHAR,
        page            VARCHAR,
        registration    FLOAT,
        sessionId       INTEGER,
        song            VARCHAR,
        status          INTEGER,
        ts              TIMESTAMP,
        userAgent       VARCHAR,
        userId          INTEGER
    )
""")

staging_songs_table_create = ("""
 CREATE TABLE staging_songs(
     artist_id        VARCHAR,
     artist_latitude  FLOAT,
     artist_location  VARCHAR,
     artist_longitude FLOAT,
     artist_name      VARCHAR,
     duration         FLOAT,
     num_songs        INTEGER,
     song_id          VARCHAR,
     title            VARCHAR,
     year             INTEGER
 )
""")

songplay_table_create = ("""
    CREATE TABLE songplay(
    songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time  TIMESTAMP NOT NULL SORTKEY DISTKEY,
    user_id     VARCHAR NOT NULL,
    level       VARCHAR,
    song_id     VARCHAR NOT NULL,
    artist_id   VARCHAR NOT NULL,
    session_id  INTEGER,
    location    VARCHAR,
    user_agent  VARCHAR
    )
""")

user_table_create = ("""
    CREATE TABLE users(
    user_id    INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR,
    last_name  VARCHAR,
    gender     VARCHAR,
    level      VARCHAR
    )
""")

song_table_create = ("""
    CREATE TABLE song(
    song_id    VARCHAR NOT NULL SORTKEY PRIMARY KEY,
    title      VARCHAR,
    artist_id  VARCHAR,
    year       INTEGER,
    duration   FLOAT
    )
""")

artist_table_create = ("""
    CREATE TABLE artist(
    artist_id VARCHAR NOT NULL SORTKEY PRIMARY KEY,
    name      VARCHAR NOT NULL,
    location  VARCHAR,
    latitude FLOAT,
    longitude FLOAT
    )
""")

time_table_create = ("""
    CREATE TABLE time 
    (
    start_time TIMESTAMP NOT NULL DISTKEY SORTKEY PRIMARY KEY,
    hour       INTEGER,
    day        INTEGER, 
    week       INTEGER,
    month      INTEGER,
    year       INTEGER,
    weekday    VARCHAR
    )
    
""")

# STAGING TABLES
staging_events_copy = ("""
    copy staging_events from {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON {log_json_path}
    timeformat as 'epochmillisecs';
""").format(data_bucket=config['S3']['LOG_DATA'],role_arn=config['IAM_ROLE']['ARN'],log_json_path=config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    copy staging_songs from {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON 'auto';
""").format(data_bucket=config['S3']['SONG_DATA'],role_arn=config['IAM_ROLE']['ARN'])

# FINAL TABLES
songplay_table_insert = ("""
    INSERT INTO songplay (start_time,user_id,level,song_id,artist_id,session_id,location,user_agent)
    SELECT distinct 
    events.ts AS start_time,
    events.userId as user_id,
    events.level as level,
    songs.song_id as song_id,
    songs.artist_id as artist_id,
    events.sessionId as session_id,
    events.location as location,
    events.userAgent as user_agent
    from 
    staging_events events 
    JOIN
    staging_songs songs
    ON 
    (events.song = songs.title AND events.artist = songs.artist_name
    and
    events.length = songs.duration
    )
    AND events.page = 'NextSong'
""")
    
user_table_insert = ("""
    INSERT INTO users (user_id,first_name,last_name,gender,level)
    SELECT  
    distinct(userId) AS user_id,
    firstName as first_name,
    lastName as last_name,
    gender as gender,
    level as level
    from staging_events
    where userId is NOT NULL
    AND page  =  'NextSong';
""")

song_table_insert = ("""
    INSERT INTO song (song_id,title,artist_id,year,duration)
    SELECT 
    distinct(song_id) as song_id,
    title as title, 
    artist_id as artist_id,
    year as year,
    duration as duration
    from staging_songs
    where song_id is NOT NULL
""")

artist_table_insert = ("""
    INSERT INTO artist (artist_id,name,location,latitude,longitude)
    SELECT 
    distinct(artist_id) as artist_id,
    artist_name as name,
    artist_location as location,
    artist_latitude as latitude,
    artist_longitude as longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT  
    distinct(start_time) as start_time,
    EXTRACT(hour FROM start_time) as hour,
    EXTRACT(day FROM start_time) as day,
    EXTRACT(week FROM start_time) as week,
    EXTRACT(month FROM start_time) as month,
    EXTRACT(year FROM start_time) as year,
    EXTRACT(dayofweek FROM start_time) as weekday
    FROM songplay;
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create,songplay_table_create,user_table_create,song_table_create,artist_table_create,time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop,user_table_drop,song_table_drop,artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert,user_table_insert,song_table_insert,artist_table_insert,time_table_insert]
