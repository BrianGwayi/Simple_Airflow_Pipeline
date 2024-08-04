# Simple_Airflow_Pipeline
#### Project Brief 

Scrap xml data feed   
Parse the xml feed   
Transform   
Load to PostgreSQL database    
Orchestration - Apache Airflow

**Code**   
[.py elt_code](elt_pipeline.py)     

![End_Goal](assets/imgs/ui_webserver.png)     

![End_Goal](assets/imgs/end_goal.png)     

![End_Goal](assets/imgs/tab.png)   

Resources   
XML FEEDs - URLs   

[Kenya RSS Feed - https://www.myjobmag.co.ke/aggregate_feed.xml](https://www.myjobmag.co.ke/aggregate_feed.xml)        
[Ghana RSS Feed - https://www.myjobmagghana.com/aggregate_feed.xml](https://www.myjobmagghana.com/aggregate_feed.xml)   
[South Africa RSS Feed - https://www.myjobmag.co.za/aggregate_feed.xml](https://www.myjobmag.co.za/aggregate_feed.xml)    
[Nigeria RSS Feed- https://www.myjobmag.com/aggregate_feed.xml](https://www.myjobmag.com/aggregate_feed.xml)   

# Areas of Improvement
### Staging Area
Example AWS s3 bucket
```
def create_bucket(bucket_name, region=None):
    try:
        if region is None:
        client = boto3.client(s3)
        client = boto3.client(s3, region_name=region)
        client.create_bucket(Bucket=bucket_name)
        else
        location = {LocationConstraint:region}
        client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    execpt
        logging.error(e)
        return False
    return True
```
### Pandas Chaining Method
Chaining method is a way to join multiple operations in concise and expressive way.   
It allows us to link together a sequence of transformation and cleaning steps.   
Chaining method in action  
```
def alter(df):
    df = (response
           .drop("salary", axis=1)
           .drop_duplicates("link", keep='first')
           .rename({"id":"jid"}, axis=1)
           .astype({"jid":"int64","pubDate":"datetime64[ns]"})
           .sort_values("jid", ascending=False)
           .query("jid > 768100")
           .assign(country="Kenya")
           .assign(trial= lambda x:x.jid*10))
    return df
alter(df)
```

