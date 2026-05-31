import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"
sql_processing_customer_dir = Path("./sql_relevant/processing_customer.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

customer = pd.read_csv(bronze_dir + 'customer/ingestion_20_05_2026/customer.tbl', storage_options=storage_options,
                       sep='|', header=None)

print(customer.head())
print('=' * 150)
print(customer.info())

customer = customer.drop(columns=customer.columns[8])
print(customer.head())
print('=' * 150)

customer.columns = ['c_custkey', 'c_name', 'c_address', 'c_nationkey', 'c_phone', 'c_acctbal', 'c_mktsegment',
                    'c_comment']
print(customer.head())
print(customer.info())

customer['c_name'] = customer['c_name'].astype('string')
customer['c_address'] = customer['c_address'].astype('string')
customer['c_phone'] = customer['c_phone'].astype('string')
customer['c_mktsegment'] = customer['c_mktsegment'].astype('string')
customer['c_comment'] = customer['c_comment'].astype('string')

customer = customer.dropna(subset=['c_phone']).reset_index(drop=True)
print(customer.info())

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

connection.register('customer_bronzeLayer', customer)

sql_processing_customer = sql_processing_customer_dir.read_text()
connection.execute(sql_processing_customer)

silver_customer = pd.read_parquet('s3://silver/customer/ingestion_20_05_2026/customer.parquet',
                                  storage_options=storage_options)

print(silver_customer.head())
print(silver_customer.info())
