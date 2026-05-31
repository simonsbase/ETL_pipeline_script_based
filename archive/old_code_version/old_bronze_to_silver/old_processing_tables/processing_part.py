import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"

sql_processing_part_dir = Path("./sql_relevant/processing_part.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

part = pd.read_excel(bronze_dir + 'part/ingestion_20_05_2026/part.xlsx', storage_options=storage_options)

print(part.head())
print('=' * 150)
print(part.info())
print('=' * 150)

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

part['p_name'] = part['p_name'].astype('string')
part['p_mfgr'] = part['p_mfgr'].astype('string')
part['p_brand'] = part['p_brand'].astype('string')
part['p_type'] = part['p_type'].astype('string')
part['p_container'] = part['p_container'].astype('string')
part['p_comment'] = part['p_comment'].astype('string')

connection.register('part_bronzeLayer', part)

sql_processing_part = sql_processing_part_dir.read_text()
connection.execute(sql_processing_part)

silver_part = pd.read_parquet('s3://silver/part/ingestion_20_05_2026/part.parquet', storage_options=storage_options)

print(silver_part.head())
print(silver_part.info())
