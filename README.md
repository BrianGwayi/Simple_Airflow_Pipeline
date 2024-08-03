# Simple_Airflow_Pipeline
#### Project Brief   
Myjobmag is a job listing company that efficiently connect great candidates to great companies at all levels while constantly developing both ends of the marketplace in diverse functional areas.
Myjobmag shares job related information through a standardised xml job feed. The xml job feed returns 100 most recent job lisitng on a rollup basis, deleting old lsiting when new a listing is available. 

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
*Set up Postres SQL database  
*Extract - xml_feed >> Kenya,  Ghana,  South Africa,  Nigeria   
* Transform - xml_feed    
* Merge feeds from Kenya,  Ghana,  South Africa,  Nigeria  
* Get delta data   
* Load - delta to PostgreSQL  
* Build History - way past 100 listing

#### End Goal:    


