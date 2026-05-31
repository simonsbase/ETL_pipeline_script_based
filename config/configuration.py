import pandas as pd

# 设置全局pands输出总宽度与列宽度
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

ingestion_date = 'ingestion_20_05_2026'

# 访问MinIO用户名与密码及端口
minio_key = 'admin'
minio_sec = 'Admin123456!'
minio_port = 'localhost:9000'
minio_url = 'http://localhost:9000'

# MinIO各层目录
bronze_dir = 's3://bronze/'
silver_dir = 's3://silver/'
gold_dir = 's3://gold/'

# Pandas用于访问MinIO的参数包
storage_options = {'key': minio_key, 'secret': minio_sec, 'client_kwargs': {'endpoint_url': minio_url}}

# DuckDB用于访问MinIO的参数包
config_minio = f'''
set s3_access_key_id='{minio_key}';
set s3_secret_access_key='{minio_sec}';
set s3_endpoint='{minio_port}';

set s3_use_ssl=false;
set s3_url_style='path';
'''
