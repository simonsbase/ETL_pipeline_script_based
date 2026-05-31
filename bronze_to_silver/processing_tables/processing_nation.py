import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_nation_dir = Path("./sql_relevant/processing_nation.sql")
output_dir = 's3://silver/nation/ingestion_20_05_2026/nation.parquet'

nation = pd.read_json(bronze_dir + 'nation/ingestion_20_05_2026/nation.json', storage_options=storage_options)

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
nation['n_name'] = nation['n_name'].astype('string')
nation['n_comment'] = nation['n_comment'].astype('string')

connection = run_sql_job(sql_processing_nation_dir, 'nation_bronzeLayer', nation)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
