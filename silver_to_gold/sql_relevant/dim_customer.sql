copy
    (
    /*
    1.从MinIOs的ilver层读取相关表
    2.构造customer维度表
    3.将该表导入MinIO的gold层
    */
    with customer as (select *
                       from read_parquet('s3://silver/customer/ingestion_20_05_2026/customer.parquet')),

          nation as (select *
                     from read_parquet('s3://silver/nation/ingestion_20_05_2026/nation.parquet')),

          region as (select *
                     from read_parquet('s3://silver/region/ingestion_20_05_2026/region.parquet')),

          dim_customer as (select c_custkey,
                                  c_name,
                                  c_acctbal,
                                  c_mktsegment,
                                  n_nationkey,
                                  n_name,
                                  r_regionkey,
                                  r_name
                           from customer
                                    join nation on c_nationkey = n_nationkey
                                    join region on n_regionkey = r_regionkey)

     select *
     from dim_customer)
    to 's3://gold/dim_customer/ingestion_20_05_2026/dim_customer.parquet'
    (FORMAT parquet, OVERWRITE true);