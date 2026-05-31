import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_supplier_dir = Path("./sql_relevant/processing_supplier.sql")
output_dir = 's3://silver/supplier/ingestion_20_05_2026/supplier.parquet'

supplier = pd.read_excel(bronze_dir + 'supplier/ingestion_20_05_2026/supplier.xlsx', storage_options=storage_options)

# 把s_name列中不同长度的空字符串缩短为统一长度的空字符串，便于后续处理
supplier['s_name'] = supplier['s_name'].str.strip()
supplier['s_name'] = supplier['s_name'].replace('', pd.NA)

# 把s_phone列中不同长度的空字符串缩短为统一长度的空字符串，便于后续处理
supplier['s_phone'] = supplier['s_phone'].str.strip()
supplier['s_phone'] = supplier['s_phone'].replace('', pd.NA)

supplier = supplier.dropna(subset=['s_name']).reset_index(drop=True)
supplier = supplier.dropna(subset=['s_phone']).reset_index(drop=True)

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
supplier['s_name'] = supplier['s_name'].astype('string')
supplier['s_address'] = supplier['s_address'].astype('string')
supplier['s_phone'] = supplier['s_phone'].astype('string')
supplier['s_comment'] = supplier['s_comment'].astype('string')

connection = run_sql_job(sql_processing_supplier_dir, 'supplier_bronzeLayer', supplier)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
