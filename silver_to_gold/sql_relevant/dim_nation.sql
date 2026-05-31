copy
    (
        /*
    1.从MinIOs的ilver层读取相关表
    2.构造nation维度表
    3.将该表导入MinIO的gold层
    */
    with nation as (select *
                    from read_parquet('s3://silver/nation/ingestion_20_05_2026/nation.parquet')),
         region as (select *
                    from read_parquet('s3://silver/region/ingestion_20_05_2026/region.parquet'))

    select n_nationkey, n_name, r_regionkey, r_name
    from nation
             join region on n_regionkey = r_regionkey
    )
    TO 's3://gold/dim_nation/ingestion_20_05_2026/dim_nation.parquet'
    (FORMAT parquet, OVERWRITE true);