import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"
sql_processing_orders_dir = Path("./sql_relevant/processing_orders.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

orders = pd.read_table(bronze_dir + 'orders/ingestion_20_05_2026/orders.tsv', storage_options=storage_options)

print(orders.head())
print('=' * 150)
print(orders.info())

print(orders.loc[orders['o_orderdate'] == '0000-00-00'])
print('=' * 150)
print(orders.loc[orders['o_orderdate'] == '0000-00-00'].count())

orders['o_orderdate'] = orders['o_orderdate'].replace('0000-00-00', pd.NA)
print(orders.loc[orders['o_orderdate'] == '0000-00-00'].count())
print('=' * 150)

orders = orders.dropna(subset='o_orderdate').reset_index(drop=True)
print(orders.describe())
print('=' * 150)

print(orders.describe())
print('=' * 150)

print(orders.loc[orders['o_totalprice'] <= 0])
print('=' * 150)

orders = orders.loc[orders['o_totalprice'] > 0].reset_index(drop=True)
print(orders.info())
print('=' * 150)

print(orders.describe())
print('=' * 150)

orders['o_orderstatus'] = orders['o_orderstatus'].astype('string')

orders['o_orderdate'] = pd.to_datetime(orders['o_orderdate'])

orders['o_orderpriority'] = orders['o_orderpriority'].astype('string')
orders['o_clerk'] = orders['o_clerk'].astype('string')
orders['o_comment'] = orders['o_comment'].astype('string')

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

connection.register('orders_bronzeLayer', orders)

sql_processing_orders = sql_processing_orders_dir.read_text()
connection.execute(sql_processing_orders)

silver_orders = pd.read_parquet('s3://silver/orders/ingestion_20_05_2026/orders.parquet',
                                storage_options=storage_options)

print(silver_orders.head())
print(silver_orders.info())
