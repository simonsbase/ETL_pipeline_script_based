import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_region_dir = Path('./sql_relevant/processing_region.sql')
output_dir = 's3://silver/region/ingestion_20_05_2026/region.parquet'

region = pd.read_json(bronze_dir + 'region/ingestion_20_05_2026/region.json', storage_options=storage_options)

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
region['r_name'] = region['r_name'].astype('string')
region['r_comment'] = region['r_comment'].astype('string')

connection = run_sql_job(sql_processing_region_dir, 'region_bronzeLayer', region)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
