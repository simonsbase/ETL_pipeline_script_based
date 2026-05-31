import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"
sql_processing_nation_dir = Path("./sql_relevant/processing_nation.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

nation = pd.read_json(bronze_dir + 'nation/ingestion_20_05_2026/nation.json', storage_options=storage_options)

print(nation.head())
print('=' * 150)
print(nation.info())

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

nation['n_name'] = nation['n_name'].astype('string')
nation['n_comment'] = nation['n_comment'].astype('string')

connection.register('nation_bronzeLayer', nation)

sql_processing_nation = sql_processing_nation_dir.read_text()
connection.execute(sql_processing_nation)

silver_nation = pd.read_parquet('s3://silver/nation/ingestion_20_05_2026/nation.parquet',
                                storage_options=storage_options)

print(silver_nation.head())
print(silver_nation.info())
