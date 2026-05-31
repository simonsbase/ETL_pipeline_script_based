create or replace table mart_monthly_sales as
select *
from read_parquet('s3://gold/marts/mart_monthly_sales/ingestion_20_05_2026/mart_monthly_sales.parquet');

create or replace table mart_product_performance as
select *
from read_parquet('s3://gold/marts/mart_product_performance/ingestion_20_05_2026/mart_product_performance.parquet');

create or replace table mart_sales_each_region as
select *
from read_parquet('s3://gold/marts/mart_sales_each_region/ingestion_20_05_2026/mart_sales_each_region.parquet');

create or replace table mart_supplier_performance as
select *
from read_parquet('s3://gold/marts/mart_supplier_performance/ingestion_20_05_2026/mart_supplier_performance.parquet');