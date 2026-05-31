copy
    (
    /*
     由于region表较简单，我们直接将其导入gold层
    */
    with dim_region as (select *
                        from read_parquet('s3://silver/region/ingestion_20_05_2026/region.parquet'))

    select *
    from dim_region
    )
    TO 's3://gold/dim_region/ingestion_20_05_2026/dim_region.parquet'
    (FORMAT parquet, OVERWRITE true);