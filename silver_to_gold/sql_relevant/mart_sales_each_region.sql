copy (
          /*
     1.基于sales事实表与customer维度表，构造各区域sales指标表
     2.将其导入gold层
    */
    with fact_sales as (select *
                        from read_parquet('s3://gold/fact_sales/ingestion_20_05_2026/fact_sales.parquet')),

         dim_customer as (select *
                          from read_parquet('s3://gold/dim_customer/ingestion_20_05_2026/dim_customer.parquet'))

    select r_name,
           n_name,
           c_mktsegment,
           count(*)                      as line_count,
           count(distinct fs.o_orderkey) as order_count,
           count(distinct fs.o_custkey)  as customer_count,
           sum(fs.l_quantity)            as total_quantity,
           sum(fs.l_extendedprice)       as total_sales,
           sum(fs.discount_amount)       as total_discount_amount,
           sum(fs.discount_price)        as total_discount_sales,
           sum(fs.tax_amount)            as total_tax_amount,
           sum(fs.plus_tax_price)        as total_plus_tax_sales
    from fact_sales as fs
             join dim_customer as dc on fs.o_custkey = dc.c_custkey
    group by dc.r_name, dc.n_name, dc.c_mktsegment
    order by dc.r_name, dc.n_name, dc.c_mktsegment, total_discount_sales desc
    )
    to 's3://gold/marts/mart_sales_each_region/ingestion_20_05_2026/mart_sales_each_region.parquet'
    (FORMAT parquet, OVERWRITE true);