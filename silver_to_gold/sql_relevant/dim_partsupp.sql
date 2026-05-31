copy
    (
    /*
     由于partsupp表较简单，我们直接将其导入gold层
    */
    with dim_partsupp AS (select *
                           from read_parquet('s3://silver/partsupp/ingestion_20_05_2026/partsupp.parquet'))

     select ps_partkey, ps_suppkey, ps_availqty, ps_supplycost
     from dim_partsupp)
    to 's3://gold/dim_partsupp/ingestion_20_05_2026/dim_partsupp.parquet'
    (FORMAT parquet, OVERWRITE true);