import subprocess
import sys
import time
import csv
import duckdb
from config.configuration import config_minio, ingestion_date

bronze_to_silver_scripts = ['processing_region.py', 'processing_nation.py', 'processing_supplier.py',
                            'processing_customer.py',
                            'processing_part.py', 'processing_partsupp.py', 'processing_orders.py',
                            'processing_lineitem.py']

silver_to_gold_scripts = ['processing_dim_customer.py', 'processing_dim_nation.py', 'processing_dim_part.py',
                          'processing_dim_partsupp.py', 'processing_dim_region.py', 'processing_dim_supplier.py',
                          'processing_fact_sales.py', 'processing_mart_monthly_sales.py',
                          'processing_mart_product_performance.py',
                          'processing_mart_sales_each_region.py', 'processing_mart_supplier_performance.py']

tables_bronze_to_silver_dir = './results/tables_bronze_to_silver.csv'
tables_silver_to_gold_dir = './results/tables_silver_to_gold.csv'


def main():
    '''
    依次构造循环，依次执行每个阶段对每个表格的处理，并计算时间与查询表格行数
    :return:
    '''
    for script in bronze_to_silver_scripts:
        start = time.perf_counter()

        subprocess.run([sys.executable, 'processing_tables/' + script], cwd='../bronze_to_silver', check=True)

        end = time.perf_counter()
        s_time = end - start

        connection = duckdb.connect()
        connection.execute(config_minio)

        s_name = script.replace('processing_', '').replace('.py', '')
        s3_dir = 's3://silver/' + s_name + '/ingestion_20_05_2026/' + s_name + '.parquet'

        line_cnt = connection.execute(f"select count(*) from read_parquet('{s3_dir}')").fetchone()[0]

        avg_line = line_cnt / s_time

        print(
            'bronze_to_silver - ' + script + '执行时间（单位/秒）：' + str(s_time) + ',每秒处理数据行数：' + str(avg_line))

        with open(tables_bronze_to_silver_dir, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([script, s_time, avg_line])

    for script in silver_to_gold_scripts:
        start = time.perf_counter()

        subprocess.run([sys.executable, 'processing_tables/' + script], cwd='../silver_to_gold', check=True)

        end = time.perf_counter()
        s_time = end - start

        connection = duckdb.connect()
        connection.execute(config_minio)

        s_name = script.replace('processing_', '').replace('.py', '')

        if s_name.startswith('mart_'):
            s3_dir = 's3://gold/marts/' + s_name + '/ingestion_20_05_2026/' + s_name + '.parquet'
        else:
            s3_dir = 's3://gold/' + s_name + '/ingestion_20_05_2026/' + s_name + '.parquet'

        line_cnt = connection.execute(f"select count(*) from read_parquet('{s3_dir}')").fetchone()[0]

        avg_line = line_cnt / s_time

        print('silver_to_gold - ' + script + '执行时间（单位/秒）：' + str(s_time) + ',每秒处理数据行数：' + str(avg_line))

        with open(tables_silver_to_gold_dir, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([script, s_time, avg_line])

    subprocess.run([sys.executable, 'export_from_gold_to_warehouse.py'], cwd='../', check=True)


if __name__ == '__main__':
    main()
