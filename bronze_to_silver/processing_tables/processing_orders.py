import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_orders_dir = Path("./sql_relevant/processing_orders.sql")
output_dir = 's3://silver/orders/ingestion_20_05_2026/orders.parquet'

orders = pd.read_table(bronze_dir + 'orders/ingestion_20_05_2026/orders.tsv', storage_options=storage_options)

# 将空日期0000-00-00替换为pandas内置空值，便于后续处理
orders['o_orderdate'] = orders['o_orderdate'].replace('0000-00-00', pd.NA)
orders = orders.dropna(subset=['o_orderdate']).reset_index(drop=True)
orders = orders.loc[orders['o_totalprice'] > 0].reset_index(drop=True)

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
orders['o_orderstatus'] = orders['o_orderstatus'].astype('string')
orders['o_orderdate'] = pd.to_datetime(orders['o_orderdate'])
orders['o_orderpriority'] = orders['o_orderpriority'].astype('string')
orders['o_clerk'] = orders['o_clerk'].astype('string')
orders['o_comment'] = orders['o_comment'].astype('string')

connection = run_sql_job(sql_processing_orders_dir, 'orders_bronzeLayer', orders)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
