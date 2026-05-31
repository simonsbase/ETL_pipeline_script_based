from pathlib import Path
from utils.utils_duckdb import run_sql_job, view_table

sql_mart_product_performance_dir = Path("./sql_relevant/mart_product_performance.sql")
output_dir = 's3://gold/marts/mart_product_performance/ingestion_20_05_2026/mart_product_performance.parquet'

connection = run_sql_job(sql_mart_product_performance_dir)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
