from pathlib import Path
from utils.utils_duckdb import run_sql_job, view_table

sql_dim_partsupp_dir = Path("./sql_relevant/dim_partsupp.sql")
output_dir = 's3://gold/dim_partsupp/ingestion_20_05_2026/dim_partsupp.parquet'

connection = run_sql_job(sql_dim_partsupp_dir)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
