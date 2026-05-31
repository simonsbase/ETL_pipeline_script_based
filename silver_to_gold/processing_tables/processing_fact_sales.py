from pathlib import Path
from utils.utils_duckdb import run_sql_job, view_table

sql_fact_sales_dir = Path("./sql_relevant/fact_sales.sql")
output_dir = 's3://gold/fact_sales/ingestion_20_05_2026/fact_sales.parquet'

connection = run_sql_job(sql_fact_sales_dir)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
