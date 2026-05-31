copy (
     /*
     1.从silver层读取相关表
     2.构造supplier维度表
     3.将该维度表导入gold层
    */
    with supplier as (select *
                      from read_parquet('s3://silver/supplier/ingestion_20_05_2026/supplier.parquet')),

         nation as (select *
                    from read_parquet('s3://silver/nation/ingestion_20_05_2026/nation.parquet')),

         region as (select *
                    from read_parquet('s3://silver/region/ingestion_20_05_2026/region.parquet')),

         dim_supplier as (select s_suppkey, s_name, s_acctbal, n_nationkey, n_name, r_regionkey, r_name
                          from supplier
                                   join nation on s_nationkey = n_nationkey
                                   join region on n_regionkey = r_regionkey)

    select *
    from dim_supplier
    )
    to 's3://gold/dim_supplier/ingestion_20_05_2026/dim_supplier.parquet'
    (FORMAT parquet, OVERWRITE true);