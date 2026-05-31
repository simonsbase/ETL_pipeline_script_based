COPY (
    /*
     由于part表较简单，我们直接将其导入gold层
    */
    with dim_part as (select *
                      from read_parquet('s3://silver/part/ingestion_20_05_2026/part.parquet'))

    select p_partkey,
           p_name,
           p_mfgr,
           p_brand,
           p_type,
           p_size,
           p_container,
           p_retailprice
    from dim_part
    )
    to 's3://gold/dim_part/ingestion_20_05_2026/dim_part.parquet'
    (FORMAT parquet, OVERWRITE true);