from pathlib import Path
import duckdb
from config.configuration import config_minio
from utils.utils_duckdb import run_sql

sql_export_to_warehouse_dir = Path("./export_to_warehouse.sql")

# DuckDB数据仓库位置
warehouse_dir = './warehouse/analytics.duckdb'

# 从DuckDB连接MinIO并执行预先配置
connection = duckdb.connect(warehouse_dir)
connection.execute(config_minio)

# 执行导出sql代码
run_sql(connection, sql_export_to_warehouse_dir)

# 检查表格的处理与导入是否成功
# print(connection.execute('show tables').df())
# print('warehouse loaded:', warehouse_dir)

connection.close()
