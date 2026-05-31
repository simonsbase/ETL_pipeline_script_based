import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"
sql_processing_region_dir = Path("./sql_relevant/processing_region.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

region = pd.read_json(bronze_dir + 'region/ingestion_20_05_2026/region.json', storage_options=storage_options)

print(region.head())
print('=' * 150)
print(region.info())

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

region['r_name'] = region['r_name'].astype('string')
region['r_comment'] = region['r_comment'].astype('string')

connection.register('region_bronzeLayer', region)

sql_processing_region = sql_processing_region_dir.read_text()
connection.execute(sql_processing_region)

silver_region = pd.read_parquet('s3://silver/region/ingestion_20_05_2026/region.parquet',
                                storage_options=storage_options)

print(silver_region.head())
print(silver_region.info())
