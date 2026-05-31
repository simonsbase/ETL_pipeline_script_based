import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

sql_mart_product_performance_dir = Path("./sql_relevant/mart_product_performance.sql")

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

sql_processing_mart_product_performance = sql_mart_product_performance_dir.read_text()
connection.execute(sql_processing_mart_product_performance)

# check
df = connection.execute('''
select *
from read_parquet('s3://gold/marts/mart_product_performance/ingestion_20_05_2026/mart_product_performance.parquet') 
limit 20
''').df()

print(df)
print(df.info())
