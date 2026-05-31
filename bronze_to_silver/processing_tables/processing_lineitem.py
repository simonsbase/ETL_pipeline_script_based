import pandas as pd
from pathlib import Path
from config.configuration import bronze_dir, storage_options
from utils.utils_duckdb import run_sql_job, view_table

sql_processing_lineitem_dir = Path("./sql_relevant/processing_lineitem.sql")
output_dir = 's3://silver/lineitem/ingestion_20_05_2026/lineitem.parquet'

lineitem = pd.read_parquet(bronze_dir + 'lineitem/ingestion_20_05_2026/lineitem.parquet',
                           storage_options=storage_options)

# 由于读入之后发现所有字段皆为str类型，故参照tpc-h数据集schema重新转换类型
lineitem['l_orderkey'] = lineitem['l_orderkey'].astype('int64')
lineitem['l_partkey'] = lineitem['l_partkey'].astype('int64')
lineitem['l_suppkey'] = lineitem['l_suppkey'].astype('int64')
lineitem['l_linenumber'] = lineitem['l_linenumber'].astype('int64')

lineitem['l_quantity'] = lineitem['l_quantity'].astype('float64')
lineitem['l_extendedprice'] = lineitem['l_extendedprice'].astype('float64')
lineitem['l_discount'] = lineitem['l_discount'].astype('float64')
lineitem['l_tax'] = lineitem['l_tax'].astype('float64')

lineitem['l_shipdate'] = pd.to_datetime(lineitem['l_shipdate'])
lineitem['l_commitdate'] = pd.to_datetime(lineitem['l_commitdate'])
lineitem['l_receiptdate'] = pd.to_datetime(lineitem['l_receiptdate'])

# 由于duckdb不支持pandas的str类型，故在利用duckdb sql引擎执行sql语句之前将其转化为string类型
lineitem['l_returnflag'] = lineitem['l_returnflag'].astype('string')
lineitem['l_linestatus'] = lineitem['l_linestatus'].astype('string')
lineitem['l_shipinstruct'] = lineitem['l_shipinstruct'].astype('string')
lineitem['l_shipmode'] = lineitem['l_shipmode'].astype('string')
lineitem['l_comment'] = lineitem['l_comment'].astype('string')

connection = run_sql_job(sql_processing_lineitem_dir, 'lineitem_bronzeLayer', lineitem)

# 检查表格的处理与导入是否成功
# df = view_table(connection, output_dir, limit=10)
# print(df)
# print(df.info())

connection.close()
