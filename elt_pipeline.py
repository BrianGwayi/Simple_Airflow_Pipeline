from airflow.decorators import dag, task
from datetime import datetime, timedelta
import requests
import xmltodict
import pandas as pd
import psycopg2
from io import StringIO

@dag(
    schedule=timedelta(minutes=30),
    start_date=datetime(2024, 7, 29),
    catchup=False,
    tags=['Team B']
    )

def myjobmag_etl_pipeline():

    # [START extract]

    # Kenya
    @task()
    def gt_response_ke():
        url = "https://www.myjobmag.co.ke/aggregate_feed.xml"
        response = requests.get(url)
        feed = xmltodict.parse(response.text)
        return feed['rss']['channel']['item']
    
    # Ghana
    @task()
    def gt_response_gh():
        url = "https://www.myjobmagghana.com/aggregate_feed.xml"
        response = requests.get(url)
        feed = xmltodict.parse(response.text)
        return feed['rss']['channel']['item']
    
    # SouthAfrica
    @task()
    def gt_response_za():
        url = "https://www.myjobmag.co.za/aggregate_feed.xml"
        response = requests.get(url)
        feed = xmltodict.parse(response.text)
        return feed['rss']['channel']['item']
    
    # Nigeria
    @task()
    def gt_response_ng():
        url = "https://www.myjobmag.com/aggregate_feed.xml"
        response = requests.get(url)
        feed = xmltodict.parse(response.text)
        return feed['rss']['channel']['item']
    # [END extract]


    # [START transform]
    # Kenya
    @task()
    def tf_response_ke(gt_response_ke):
          dataframe = pd.DataFrame(gt_response_ke)
          transformed = dataframe\
            .astype({'id':'int64','pubDate':'datetime64[ns]',
                     'expiryDate':'datetime64[ns]'})\
            .drop(['salary','city_area','location','postcode',
           'contact_name','contact_email','contact_telephone'], axis=1)\
            .assign(country='Kenya')
          return transformed
    
    # Ghana
    @task()
    def tf_response_gh(gt_response_gh):
          dataframe = pd.DataFrame(gt_response_gh)
          transformed = dataframe\
            .astype({'id':'int64','pubDate':'datetime64[ns]',
                     'expiryDate':'datetime64[ns]'})\
            .drop(['salary','city_area','location','postcode',
           'contact_name','contact_email','contact_telephone'], axis=1)\
            .assign(country='Ghana')
          return transformed
    
    # SouthArfica
    @task()
    def tf_response_za(gt_response_za):
          dataframe = pd.DataFrame(gt_response_za)
          transformed = dataframe\
            .astype({'id':'int64','pubDate':'datetime64[ns]',
                     'expiryDate':'datetime64[ns]'})\
            .drop(['salary','city_area','location','postcode',
           'contact_name','contact_email','contact_telephone'], axis=1)\
            .assign(country='SouthAfrica')
          return transformed

    # Nigeria
    @task()
    def tf_response_ng(gt_response_ng):
          dataframe = pd.DataFrame(gt_response_ng)
          transformed = dataframe\
            .astype({'id':'int64','pubDate':'datetime64[ns]',
                     'expiryDate':'datetime64[ns]'})\
            .drop(['salary','city_area','location','postcode',
           'contact_name','contact_email','contact_telephone'], axis=1)\
           .assign(country='Nigeria')
          return transformed
    # [END transform]
    
    # [START merge]
    @task()
    def merge_res(tf_res_ke, tf_res_gha, tf_res_sa, tf_res_ng):
         df_row_reindex = pd.concat([tf_res_ke, tf_res_gha, tf_res_sa, tf_res_ng], ignore_index=True)
         return df_row_reindex
    # [END merge]

    # [START et delta]
    @task()
    def gt_delta (merge_res):
        conn = psycopg2.connect(
            database = "job_listing",
            user = "postgres",
            host= 'localhost',
            password = "password",
            port = 5432)
        cursor = conn.cursor()

        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(conn.get_dsn_parameters(), "\n")

        # Execute SQL Statement
        loaded=pd.read_sql("SELECT *FROM jb_posts;", conn)
        conn.close()
        delta = merge_res[~merge_res['id'].isin(loaded['id'])]
        return delta
    # [END et delta]
    
    # [START load]
    @task()
    def load_delta(gt_delta):
        #engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/listing_db")
        #connection = engine.connect()
        conn = psycopg2.connect(
            database = "job_listing",
            user = "postgres",
            host= 'localhost',
            password = "password",
            port = 5432)
        
        cursor = conn.cursor()
        buffer = StringIO()
        gt_delta.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        cursor.copy_expert("""COPY jb_posts (id, link, guid, title, position,
                introduction, company, experience, description,
                studies, industry, contract, working_hours,
                region, pubdate, expirydate, country) FROM STDIN with csv""", buffer)

        conn.commit()
        cursor.close()
        conn.close()
    # [END load]
    
    # [START set dependencies]
    gt_response_ke = gt_response_ke()
    tf_response_ke = tf_response_ke(gt_response_ke)

    gt_response_gh = gt_response_gh()
    tf_response_gh = tf_response_gh(gt_response_gh)

    gt_response_za = gt_response_za()
    tf_response_za = tf_response_za(gt_response_za)

    gt_response_ng = gt_response_ng()
    tf_response_ng = tf_response_ng(gt_response_ng)

    merge_res = merge_res(tf_response_ke, tf_response_gh, tf_response_za, tf_response_ng)

    gt_delta = gt_delta(merge_res)
    load_delta = load_delta(gt_delta)


myjobmag_etl_pipeline()