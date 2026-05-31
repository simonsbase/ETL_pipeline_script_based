from pathlib import Path
from utils.utils_duckdb import run_sql_job, view_table

sql_dim_customer_dir = Path('./sql_relevant/dim_customer.sql')
output_dir = 's3://gold/dim_customer/ingestion_20_05_2026/dim_customer.parquet'

connection = run_sql_job(sql_dim_customer_dir)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
