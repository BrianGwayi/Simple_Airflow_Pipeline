# Simple_Airflow_Pipeline
#### Project Brief 

Scrap xml data feed   
Parse the xml feed   
Transform   
Load to PostgreSQL database   

**Code**   
[.py elt_code](elt_pipeline.py)     

![End_Goal](assets/imgs/ui_webserver.png)   
![End_Goal](assets/imgs/end_goal.png)  

Resources   
XML FEEDs - URLs   

[Kenya RSS Feed - https://www.myjobmag.co.ke/aggregate_feed.xml](https://www.myjobmag.co.ke/aggregate_feed.xml)        
[Ghana RSS Feed - https://www.myjobmagghana.com/aggregate_feed.xml](https://www.myjobmagghana.com/aggregate_feed.xml)   
[South Africa RSS Feed - https://www.myjobmag.co.za/aggregate_feed.xml](https://www.myjobmag.co.za/aggregate_feed.xml)    
[Nigeria RSS Feed- https://www.myjobmag.com/aggregate_feed.xml](https://www.myjobmag.com/aggregate_feed.xml)     

#### Goals:  
* Set up Postres SQL database  
* Extract - xml_feed >> Kenya,  Ghana,  South Africa,  Nigeria   
* Transform - xml_feed    
* Merge feeds from Kenya,  Ghana,  South Africa,  Nigeria  
* Get delta data   
* Load - delta to PostgreSQL  
* Build History - way past 100 listing


