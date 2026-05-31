import pandas as pd
import duckdb
from pathlib import Path

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

sql_mart_monthly_sales_dir = Path("./sql_relevant/mart_monthly_sales.sql")

connection = duckdb.connect()

connection.execute('''
set s3_access_key_id='admin';
set s3_secret_access_key='Admin123456!';
set s3_endpoint='localhost:9000';

set s3_use_ssl=false;
set s3_url_style='path';
''')

sql_processing_mart_monthly_sales = sql_mart_monthly_sales_dir.read_text()
connection.execute(sql_processing_mart_monthly_sales)

# check
df = connection.execute('''
select *
from read_parquet('s3://gold/marts/mart_monthly_sales/ingestion_20_05_2026/mart_monthly_sales.parquet') 
limit 20
''').df()

print(df)
print(df.info())
