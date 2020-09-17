# Project Datawarehouse
___
## Project description
___

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The aim of this project is to build an ETL pipeline that extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for the analytics team to continue finding insights in what songs their users are listening to. 

## Project description
___
This project includes the following files:
- create_table.py - This is the file where the fact and dimension tables for the star schema in Redshift are created and dropped.
- etl.py  - This is the file which is where the data gets loaded from S3 into staging tables on Redshift and then processed into the dimension and fact tables  on Redshift.
- sql_queries.py - This is the file where the SQL statements (CREATE/INSERT/DROP)
- README.md  - This has details on everything about the project



#### To be able to access S3 data from your local project workspace:
___ 
You should be able to find the AWS access and secret keys in the IAM console. 

```
aws configure
> AWS Access Key ID : <enter your access key>
> AWS Secret Access Key : <enter your secret access key>
> Default region name : us-west-2
> Default output format : <enter>
```



#### Get an idea of data in the S3 location by:
___
`aws s3 ls s3://udacity-dend/log_data/2018/11/`

```
2019-04-17 12:03:13       7151 2018-11-01-events.json
2019-04-17 12:03:13      83585 2018-11-02-events.json
2019-04-17 12:03:13      54084 2018-11-03-events.json
2019-04-17 12:03:13      85671 2018-11-04-events.json
2019-04-17 12:03:13     189295 2018-11-05-events.json
2019-04-17 12:03:13      85373 2018-11-06-events.json
2019-04-17 12:03:13      97519 2018-11-07-events.json
2019-04-17 12:03:13     102218 2018-11-08-events.json
2019-04-17 12:03:13     134804 2018-11-09-events.json
2019-04-17 12:03:13      44076 2018-11-10-events.json
2019-04-17 12:03:13      43711 2018-11-11-events.json
2019-04-17 12:03:13      99854 2018-11-12-events.json
2019-04-17 12:03:13     186826 2018-11-13-events.json
2019-04-17 12:03:13     217264 2018-11-14-events.json
2019-04-17 12:03:13     243143 2018-11-15-events.json
2019-04-17 12:03:13     175491 2018-11-16-events.json
2019-04-17 12:03:13      66164 2018-11-17-events.json
2019-04-17 12:03:13      75763 2018-11-18-events.json
2019-04-17 12:03:13     150798 2018-11-19-events.json
2019-04-17 12:03:13     174991 2018-11-20-events.json
2019-04-17 12:03:13     242588 2018-11-21-events.json
2019-04-17 12:03:13      46181 2018-11-22-events.json
2019-04-17 12:03:13     138647 2018-11-23-events.json
2019-04-17 12:03:13     170219 2018-11-24-events.json
2019-04-17 12:03:13      26214 2018-11-25-events.json
2019-04-17 12:03:13     123576 2018-11-26-events.json
2019-04-17 12:03:13     141625 2018-11-27-events.json
2019-04-17 12:03:13     202910 2018-11-28-events.json
2019-04-17 12:03:13     168646 2018-11-29-events.json
2019-04-17 12:03:13     177211 2018-11-30-events.json
```

#### Get a sample of how one file looks like by:
___
`aws s3 cp s3://udacity-dend/log_data/2018/11/2018-11-01-events.json .`
`cat 2018-11-01-events.json`

#### SAMPLE : 
___
```
{
	"artist":"Fall Out Boy",
	"auth":"Logged In",
	"firstName":"Ryan",
	"gender":"M",
	"itemInSession":1,
	"lastName":"Smith",
	"length":200.72444,
	"level":"free",
	"location":"San Jose-Sunnyvale-Santa Clara, CA",
	"method":"PUT",
	"page":"NextSong",
	"registration":1541016707796.0,
	"sessionId":169,
	"song":"Nobody Puts Baby In The Corner",
	"status":200,
	"ts":1541109125796,
	"userAgent":"\"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Ubuntu Chromium\/36.0.1985.125 Chrome\/36.0.1985.125 Safari\/537.36\"",
	"userId":"26"
}
```
#### Field derivation based on sample data:
___

| Field | Type |
| ------ | ------- |
| artist| VARCHAR |
| auth | VARCHAR |
| firstName | VARCHAR |
| gender|VARCHAR|
|itemInSession|INTEGER|
|lastName|VARCHAR|
|length|FLOAT|
|level|VARCHAR|
|location|VARCHAR|
|method|VARCHAR|
|page|VARCHAR|
|registration|FLOAT|
|sessionId|INTEGER|
|song|VARCHAR|
|status|INTEGER|
|ts|TIMESTAMP|
|userAgent|VARCHAR|
|userId|VARCHAR |


#### Get an idea of data in the S3 location by:
___

`aws s3 ls s3://udacity-dend/song_data/A/A/A/`

```
2019-04-17 03:20:41        225 TRAAAAK128F9318786.json
2019-04-17 03:20:41        284 TRAAAAV128F421A322.json
2019-04-17 03:20:41        249 TRAAABD128F429CF47.json
2019-04-17 03:20:41        243 TRAAACN128F9355673.json
2019-04-17 03:20:41        289 TRAAAEA128F935A30D.json
2019-04-17 03:20:41        231 TRAAAED128E0783FAB.json
2019-04-17 03:20:41        228 TRAAAEM128F93347B9.json
2019-04-17 03:20:41        248 TRAAAEW128F42930C0.json
2019-04-17 03:20:41        225 TRAAAFD128F92F423A.json
2019-04-17 03:20:41        250 TRAAAGR128F425B14B.json
2019-04-17 03:20:41        256 TRAAAHD128F42635A5.json
2019-04-17 03:20:41        271 TRAAAHJ128F931194C.json
2019-04-17 03:20:41        263 TRAAAHZ128E0799171.json
2019-04-17 03:20:41        254 TRAAAIR128F1480971.json
2019-04-17 03:20:41        278 TRAAAJN128F428E437.json
2019-04-17 03:20:41        223 TRAAAND12903CD1F1B.json
2019-04-17 03:20:41        259 TRAAANK128F428B515.json
2019-04-17 03:20:41        303 TRAAAOF128F429C156.json
2019-04-17 03:20:41        265 TRAAAPK128E0786D96.json
2019-04-17 03:20:41        232 TRAAAQN128F9353BA0.json
2019-04-17 03:20:41        254 TRAAAQO12903CD8E1C.json
2019-04-17 03:20:41        301 TRAAAUC128F428716F.json
2019-04-17 03:20:41        249 TRAAAUR128F428B1FA.json
2019-04-17 03:20:41        253 TRAAAYL128F4271A5B.json
```

NOTE => 24 rows

#### Get a sample of how one file looks like by:
___

`aws s3 cp ss3://udacity-dend/song_data/A/A/A/TRAAAAK128F9318786.json .`

`cat TRAAAAK128F9318786.json`


#### SAMPLE : 
___
```
{
	"artist_id":"ARJNIUY12298900C91",
	"artist_latitude":null,
	"artist_location":"",
	"artist_longitude":null,
	"artist_name":"Adelitas Way",
	"duration":213.9424,
	"num_songs":1,
	"song_id":"SOBLFFE12AF72AA5BA",
	"title":"Scream",
	"year":2009
}
```

#### Field derivation based on sample data:
___

| Field | Type |
| ------ | ------- |
|artist_id|VARCHAR|
|artist_latitude|FLOAT|
|artist_location|VARCHAR|
|artist_longitude|FLOAT|
|artist_name|VARCHAR|
|duration|FLOAT|
|num_songs|INTEGER|
|song_id|VARCHAR|
|title|VARCHAR|
|year|INTEGER|

### Process for building the ETL: 
___
#### STEP 1: SET UP REDSHIFT CLUSTER IN YOUR AWS ACCOUNT

- Launch a Redshift Cluster   - Sign in to the AWS Management Console and open the Amazon Redshift console at https://console.aws.amazon.com/redshift/.
- On the Amazon Redshift Dashboard, choose Launch cluster.
- Enter the following:
    - Cluster identifier: Enter redshift-cluster.
    - Database name: Enter dev.
    - Database port: Enter 5439.
    - Master user name: Enter awsuser.
    - Master user password and Confirm password: Enter a password for the master user account.

- On the Additional Configuration page, enter the following values:
    - VPC security groups: redshift_security_group
    - Available IAM roles: myRedshiftRole
- Click Continue 
- Review your Cluster configuration and choose Launch cluster.


#### STEP 2: Test on a small set of data: 
- In your dwh.cfg file, point the SONG_DATA to: 
    - ```SONG_DATA='s3://udacity-dend/song_data/A/A/A/'```

#### STEP 3: Call the create_tables.py for 1 time create of the tables
-   ```
    python create_tables.py 
    ```

#### STEP 4: 
- Add queries in sql_queries.py to copy staging/create/insert/ tables.


#### Step 5: Run the etl (For the full dataset, this may take anywhere from 20-40 mins)
-   ```
    python etl.py 
    ```

#### Step 6: In the `query editor` section on the Redshift AWS console, choose public and verify: 

Thefollowing are final counts of the number of rows in each table:
```
select count(*) from staging_songs;
14896

select count(*) from staging_events;
8056

select count(*) from songplay;
333

select count(*) from users;
105

select count(*) from song;
14896

select count(*) from artist;
10025

select count(*) from time;
333

```
#### Step 7: When you are done, terminate the redshift-cluster


## Database schema
___

#### `STAGING TABLES`
| Tablename | Description | Fields |
| ------ | ------- | --------- |
|staging_events|staging data in redshift for events|<ul><li>artist</li><li>auth </li><li>firstName </li><li>gender </li><li>itemInSession  </li><li>lastName  </li><li>length </li><li>level</li><li>location  </li><li>method </li><li>page </li><li>registration</li><li>sessionId </li><li>song </li><li>status </li><li>ts</li><li>userAgent</li> <li>userId </li></ul>|
|staging_songs|staging data in redshift for songs|<ul><li>artist_id </li><li>artist_latitude</li><li>artist_location</li><li>artist_longitude </li><li>artist_name </li><li>duration  </li><li>num_songs </li><li>song_id</li><li>title</li><li>year </li></ul>|



#### `FACT TABLE`
    
| Tablename | Description | Fields |
| ------ | ------- | --------- |
| songplays | records in event data associated with song plays i.e. records with page NextSong | <ul><li>songplay_id</li><li>start_time</li><li>user_id</li><li>level</li><li>song_id</li><li>artist_id</li><li>session_id</li><li>location</li><li>user_agent</li></ul>|

#### `DIMENSION TABLES`

| Tablename | Description | Fields |
| ------ | ------- | --------- |
| users | users in the app | <ul> <li>user_id</li><li>first_name</li><li>last_name</li><li>gender</li><li>level </ul> |
|songs | songs in music database |  <ul> <li>song_id</li><li>title</li><li>artist_id</li><li>year</li><li>duration </ul>|
| artists | artists in music database | <ul> <li>artist_id</li><li>name</li><li>location</li><li>lattitude</li><li>longitude </ul>|
|time | timestamps of records in songplays broken down into specific units |  <ul> <li>start_time</li><li>hour</li><li>day</li><li>week</li><li>month</li><li>year</li><li>weekday </ul> |

