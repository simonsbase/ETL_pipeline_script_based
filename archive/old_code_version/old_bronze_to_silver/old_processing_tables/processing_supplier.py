import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"

sql_processing_supplier_dir = Path("./sql_relevant/processing_supplier.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

supplier = pd.read_excel(bronze_dir + 'supplier/ingestion_20_05_2026/supplier.xlsx', storage_options=storage_options)

print(supplier.head())
print('=' * 150)
print(supplier.info())
print('=' * 150)

supplier['s_name'] = supplier['s_name'].str.strip()
supplier['s_name'] = supplier['s_name'].replace('', pd.NA)
print(supplier.loc[supplier['s_name'].isna()])

print('=' * 150)

supplier['s_phone'] = supplier['s_phone'].str.strip()
supplier['s_phone'] = supplier['s_phone'].replace('', pd.NA)
print(supplier.loc[supplier['s_phone'].isna()])

supplier = supplier.dropna(subset=['s_name'])
print(supplier.info())

supplier = supplier.dropna(subset=['s_phone'])
print(supplier.info())

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

supplier['s_name'] = supplier['s_name'].astype('string')
supplier['s_address'] = supplier['s_address'].astype('string')
supplier['s_phone'] = supplier['s_phone'].astype('string')
supplier['s_comment'] = supplier['s_comment'].astype('string')

connection.register('supplier_bronzeLayer', supplier)

sql_processing_supplier = sql_processing_supplier_dir.read_text()
connection.execute(sql_processing_supplier)

silver_supplier = pd.read_parquet('s3://silver/supplier/ingestion_20_05_2026/supplier.parquet',
                                  storage_options=storage_options)

print(silver_supplier.head())
print(silver_supplier.info())
