copy (
          /*
     1.基于sales事实表与supplier维度表，构造供应商表现指标表
     2.将其导入gold层
    */
    with fact_sales as (select *
                        from read_parquet('s3://gold/fact_sales/ingestion_20_05_2026/fact_sales.parquet')),

         dim_supplier as (select *
                          from read_parquet('s3://gold/dim_supplier/ingestion_20_05_2026/dim_supplier.parquet'))

    select ds.s_suppkey,
           ds.s_name,
           ds.s_acctbal,
           ds.n_name                     as nation_name,
           ds.r_name                     as region_name,
           count(*)                      as line_count,
           count(distinct fs.o_orderkey) as order_count,
           count(distinct fs.l_partkey)  as supplied_part_count,
           sum(fs.l_quantity)            as total_quantity,
           sum(fs.l_extendedprice)       as total_sales,
           sum(fs.discount_amount)       as total_discount_amount,
           sum(fs.discount_price)        as total_discount_sales,
           sum(fs.tax_amount)            as total_tax_amount,
           sum(fs.plus_tax_price)        as total_plus_tax_sales
    from fact_sales as fs
             join dim_supplier as ds on fs.l_suppkey = ds.s_suppkey
    group by ds.s_suppkey, ds.s_name, ds.s_acctbal, ds.n_name, ds.r_name
    order by ds.s_name, ds.n_name, ds.r_name, total_discount_sales desc
    )
    to 's3://gold/marts/mart_supplier_performance/ingestion_20_05_2026/mart_supplier_performance.parquet'
    (FORMAT parquet, OVERWRITE true);