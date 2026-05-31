import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

bronze_dir = "s3://bronze/"
silver_dir = "s3://silver/"
sql_processing_lineitem_dir = Path("./sql_relevant/processing_lineitem.sql")

storage_options = {'key': 'admin', 'secret': 'Admin123456!', 'client_kwargs': {'endpoint_url': 'http://localhost:9000'}}

lineitem = pd.read_parquet(bronze_dir + 'lineitem/ingestion_20_05_2026/lineitem.parquet',
                           storage_options=storage_options)

print(lineitem.head())
print('=' * 150)
print(lineitem.info())

lineitem['l_orderkey'] = lineitem['l_orderkey'].astype('int64')
lineitem['l_partkey'] = lineitem['l_partkey'].astype('int64')
lineitem['l_suppkey'] = lineitem['l_suppkey'].astype('int64')
lineitem['l_linenumber'] = lineitem['l_linenumber'].astype('int64')

lineitem['l_quantity'] = lineitem['l_quantity'].astype('float64')
lineitem['l_extendedprice'] = lineitem['l_extendedprice'].astype('float64')
lineitem['l_discount'] = lineitem['l_discount'].astype('float64')
lineitem['l_tax'] = lineitem['l_tax'].astype('float64')

lineitem['l_returnflag'] = lineitem['l_returnflag'].astype('string')
lineitem['l_linestatus'] = lineitem['l_linestatus'].astype('string')

lineitem['l_shipdate'] = pd.to_datetime(lineitem['l_shipdate'])
lineitem['l_commitdate'] = pd.to_datetime(lineitem['l_commitdate'])
lineitem['l_receiptdate'] = pd.to_datetime(lineitem['l_receiptdate'])

lineitem['l_shipinstruct'] = lineitem['l_shipinstruct'].astype('string')
lineitem['l_shipmode'] = lineitem['l_shipmode'].astype('string')
lineitem['l_comment'] = lineitem['l_comment'].astype('string')

print(lineitem.info())

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

connection.register('lineitem_bronzeLayer', lineitem)

sql_processing_lineitem = sql_processing_lineitem_dir.read_text()
connection.execute(sql_processing_lineitem)

silver_lineitem = pd.read_parquet('s3://silver/lineitem/ingestion_20_05_2026/lineitem.parquet',
                                  storage_options=storage_options)

print(silver_lineitem.head())
print(silver_lineitem.info())
