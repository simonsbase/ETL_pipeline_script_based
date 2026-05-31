import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_customer_dir = Path('./sql_relevant/processing_customer.sql')
output_dir = 's3://silver/customer/ingestion_20_05_2026/customer.parquet'

customer = pd.read_csv(bronze_dir + 'customer/ingestion_20_05_2026/customer.tbl', storage_options=storage_options,
                       sep='|', header=None)

# 由于customer表各字段间以竖线分割，所以在读入的时候会多出一列无意义的空值
customer = customer.drop(columns=customer.columns[8])

# 读入后发现各字段无命名，故参照tpc-h数据集schema对其命名
customer.columns = ['c_custkey', 'c_name', 'c_address', 'c_nationkey', 'c_phone', 'c_acctbal', 'c_mktsegment',
                    'c_comment']

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
customer['c_name'] = customer['c_name'].astype('string')
customer['c_address'] = customer['c_address'].astype('string')
customer['c_phone'] = customer['c_phone'].astype('string')
customer['c_mktsegment'] = customer['c_mktsegment'].astype('string')
customer['c_comment'] = customer['c_comment'].astype('string')
customer = customer.dropna(subset=['c_phone']).reset_index(drop=True)

connection = run_sql_job(sql_processing_customer_dir, 'customer_bronzeLayer', customer)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
