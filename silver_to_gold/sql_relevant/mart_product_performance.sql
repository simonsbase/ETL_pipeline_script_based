copy (
          /*
     1.基于sales事实表与part维度表，构造产品表现指标表
     2.将其导入gold层
    */
    with fact_sales as (select *
                        from read_parquet('s3://gold/fact_sales/ingestion_20_05_2026/fact_sales.parquet')),

         dim_part as (select *
                      from read_parquet('s3://gold/dim_part/ingestion_20_05_2026/dim_part.parquet'))

    select dp.p_partkey,
           dp.p_name,
           dp.p_mfgr,
           dp.p_brand,
           dp.p_type,
           dp.p_size,
           dp.p_container,
           dp.p_retailprice,
           count(*)                      as line_count,
           count(distinct fs.o_orderkey) as order_count,
           sum(fs.l_quantity)            as total_quantity,
           sum(fs.l_extendedprice)       as total_sales,
           sum(fs.discount_amount)       as total_discount_amount,
           sum(fs.discount_price)        as total_discount_sales,
           sum(fs.tax_amount)            as total_tax_amount,
           sum(fs.plus_tax_price)        as total_plus_tax_sales
    from fact_sales as fs
             join dim_part as dp on fs.l_partkey = dp.p_partkey
    group by dp.p_partkey, dp.p_name, dp.p_mfgr, dp.p_brand,
             dp.p_type, dp.p_size, dp.p_container, dp.p_retailprice
    order by dp.p_partkey, dp.p_name, dp.p_mfgr, dp.p_brand, dp.p_type, dp.p_size, dp.p_container, dp.p_retailprice,
             total_discount_sales desc
    )
    to 's3://gold/marts/mart_product_performance/ingestion_20_05_2026/mart_product_performance.parquet'
    (FORMAT parquet, OVERWRITE true);