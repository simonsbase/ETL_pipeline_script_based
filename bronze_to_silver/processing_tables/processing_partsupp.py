import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_partsupp_dir = Path("./sql_relevant/processing_partsupp.sql")
output_dir = 's3://silver/partsupp/ingestion_20_05_2026/partsupp.parquet'

partsupp = pd.read_csv(bronze_dir + 'partsupp/ingestion_20_05_2026/partsupp.csv', storage_options=storage_options)

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
partsupp['ps_comment'] = partsupp['ps_comment'].astype('string')

connection = run_sql_job(sql_processing_partsupp_dir, 'partsupp_bronzeLayer', partsupp)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
