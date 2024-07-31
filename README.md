# Simple_Airflow_Pipeline
## Simple Job Listing Datapipeline
Project Brief   
Myjobmag is a job listing company that efficiently connect great candidates to great companies at all levels while constantly developing both ends of the marketplace in diverse functional areas.
Myjobmag shares job related information through a standardised xml job feed. The xml job feed returns 100 most recent job lisitng on a rollup basis, deleting old lsiting when new a listing is available. 

XML FEEDs - URLs   
[Summarized RSS Feed - https://www.myjobmag.co.ke/jobsxml.xml](https://www.myjobmag.co.ke/jobsxml.xml)  
[Detailed RSS Feed - https://www.myjobmag.co.ke/jobsxml_by_categories.xml](https://www.myjobmag.co.ke/jobsxml_by_categories.xml) 
[Aggregate Feed - https://www.myjobmag.co.ke/aggregate_feed.xml](https://www.myjobmag.co.ke/aggregate_feed.xml)    

### Goals:  
Set up Postres SQL database  
Extract - xml_feed   
Transform - xml_feed 
Get delta - new job lisitngs added
Load - delta to PostgreSQL  
Build History - way past 100 listing

## End Goal - Job Listings in PostgreSQL Database
![End_Goal](assets/imgs/end_goal.png)

## Extract - xml_feed
Import Required Libraries
```
from airflow.decorators import dag, tasks
from datetime import datetime, timedelta
from IO import StringIO
import pandas as pd
import requests
import psyscopg2
import xmltodict
```
Default Arguments - An example containing all parameters   
```
default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'email': 'airflow@example.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': False,
    'max_retry_delay': timedelta(hours=1),
    'start_date': datetime(2024, 1, 1),
    'end_date': datetime(2024, 12, 31),
    'schedule_interval': '@daily',
    'catchup': False,
    'sla': timedelta(hours=2),
    'execution_timeout': timedelta(minutes=30),
    'queue': 'default',
    'priority_weight': 1,
    'wait_for_downstream': True,
    'trigger_rule': 'all_success',
    'pool': 'default_pool'
}
```

Instatiate a DAG
```
@dag(
schedule=None,
start_date=datetime(2024,7,30),
catch_up=False,
tags=["Team A"],
)
```
[START Extract Task]
```
@task()
def gt_response():
  url = "https://www.myjobmag.co.ke/aggregate_feed.xml"
  xml_feed = response.get(url)
  response = xmltodict.parse(xml_feed.text)
  return response['rss']['channel']['item']
```
## Transform - xml_feed
[START Transform Task]
```
@task()
def tf_response():
  tf_response = DataFrame(gt_response)
  tf_response = tf_response.\
    astype({'id':'int64','pubDate':'datetime64[ns]','expiryDate':'datetime64[ns]'}).\
    drop(['salary','city_area','location','postcode','contact_name',
          'contact_detail','contact_telephone'], axis=1)
  return tf_response
```
## Get Delta
[START Load Task]
```
@task()
def recent_response(transform_response):

  # Establish Connection to PostgreSQL Database
  conn = psycopg2.connect(
            database = Variable.get("DB_NAME"),
            user = Varibale.get("POSTGRES_USER"),
            host = "remote_db",
            password = Variable.get("POSTGRES_PASSWORD"),
            port = 5432
            )
  cursor = conn.cursor()

  # Print PostgreSQL details
  print("PostgreSQL server information")
  print(conn.get_dsn_parameters(), "\n")

  # Execute SQL Statement
  loaded=pd.read_sql("SELECT *FROM jb_listing;", conn)
  conn.close()

  # Get delta (records not loaded)
  delta = tf_response[~tf_response['id'].isin(loaded['jid'])]

  return delta

```
## Load Delta - new job listings added
```
@task()
def load_delta():
buffer = StringIO()
load_response.to_csv(buffer, index=False, header=False)
buffer.seek(0)
  cursor.copy_expert("""COPY jb_listing (jid, jlink, guid, title, job_position,
                  introduction, company, experience, description,
                  studies, industry, contract, working_hours,
                  region, pubdate, expirydate) FROM STDIN with csv""", buffer)
  conn.commit()
  cursor.close()
  conn.close()
```
[SET Dependencies]
```
gt_response = gt_response()
tf_response = tf_response(gt_response)
gt_delta = gt_delta(tf_response)
load_delta = load_delta(gt_delta)
```
[START Airflow Webserver]
```
airflow webserver -p 8080
airflow scheduler
```
## Airflow Webserver UI
![End_Goal](assets/imgs/webserver_ui.png)

