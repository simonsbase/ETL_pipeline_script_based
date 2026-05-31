import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"
sql_processing_partsupp_dir = Path("./sql_relevant/processing_partsupp.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

partsupp = pd.read_csv(bronze_dir + 'partsupp/ingestion_20_05_2026/partsupp.csv', storage_options=storage_options)

print(partsupp.head())
print('=' * 150)
print(partsupp.info())

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

partsupp['ps_comment'] = partsupp['ps_comment'].astype('string')

connection.register('partsupp_bronzeLayer', partsupp)

sql_processing_partsupp = sql_processing_partsupp_dir.read_text()
connection.execute(sql_processing_partsupp)

silver_partsupp = pd.read_parquet('s3://silver/partsupp/ingestion_20_05_2026/partsupp.parquet',
                                  storage_options=storage_options)

print(silver_partsupp.head())
print(silver_partsupp.info())
