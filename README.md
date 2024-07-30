# Simple_Airflow_Pipeline
## Simple Job Listing Datapipeline
Site: myjobmag.co.ke  
Myjobmag is a job listing company that efficiently connect great candidates to great companies at all levels while constantly developing both ends of the marketplace in diverse functional areas.
Myjobmag shares job related through a standardised xml job feed. The xml job feed returns 100 most recent job lisitng,the oldest job listings are deleted whenever most recent jobs are available on a rollup basis. 

Uniform Resource Locators - URLs  
[Summarized RSS Feed - https://www.myjobmag.co.ke/jobsxml.xml](https://www.myjobmag.co.ke/jobsxml.xml)  
[Detailed RSS Feed - https://www.myjobmag.co.ke/jobsxml_by_categories.xml](https://www.myjobmag.co.ke/jobsxml_by_categories.xml)  
[Aggregate Feed - https://www.myjobmag.co.ke/aggregate_feed.xml](https://www.myjobmag.co.ke/aggregate_feed.xml)    

Goals:  
Set up Postres SQL database  
Extract - xml_feed   
Transform - xml_feed  
Load - xml_feed to PostgreSQL  

## End Goal - Job Listings in PostgreSQL Database
![End_Goal](assets/imgs/end_goal.png)

## Extract - xml_feed
### Import Required Libraries
```
from airflow.decorators import dag, tasks
from datetime import datetime, timedelta
from IO import StringIO
import pandas as pd
import requests
import psyscopg2
import xmltodict
```
### Instatiate a DAG
```
@dag(
schedule=None,
start_date=datetime(2024,7,30),
catch_up=False,
tags=["Team A"],
)
```
### [START Extract Task]
```
@task()
def gt_response():
  url = "https://www.myjobmag.co.ke/aggregate_feed.xml"
  xml_feed = response.get(url)
  response = xmltodict.parse(xml_feed.text)
  return response['rss']['channel']['item']
``
[]()
