import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_part_dir = Path("./sql_relevant/processing_part.sql")
output_dir = 's3://silver/part/ingestion_20_05_2026/part.parquet'

part = pd.read_excel(bronze_dir + 'part/ingestion_20_05_2026/part.xlsx', storage_options=storage_options)

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
part['p_name'] = part['p_name'].astype('string')
part['p_mfgr'] = part['p_mfgr'].astype('string')
part['p_brand'] = part['p_brand'].astype('string')
part['p_type'] = part['p_type'].astype('string')
part['p_container'] = part['p_container'].astype('string')
part['p_comment'] = part['p_comment'].astype('string')

connection = run_sql_job(sql_processing_part_dir, 'part_bronzeLayer', part)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
