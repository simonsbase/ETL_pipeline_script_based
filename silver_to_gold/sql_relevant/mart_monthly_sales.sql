copy (
     /*
     1.基于sales事实表，构造月度sales指标表
     2.将其导入gold层
    */
    with fact_sales as (select *
                        from read_parquet('s3://gold/fact_sales/ingestion_20_05_2026/fact_sales.parquet'))

    select cast(date_trunc('month', o_orderdate) as date) as order_month,
           count(*)                                       as line_count,
           count(distinct o_orderkey)                     as order_count,
           count(distinct o_custkey)                      as customer_count,
           sum(l_quantity)                                as total_quantity,
           sum(l_extendedprice)                           as total_sales,
           sum(discount_amount)                           as total_discount_amount,
           sum(discount_price)                            as total_discount_sales,
           sum(tax_amount)                                as total_tax_amount,
           sum(plus_tax_price)                            as total_plus_tax_sales
    from fact_sales
    group by cast(date_trunc('month', o_orderdate) as date)
    order by order_month
    )
    to 's3://gold/marts/mart_monthly_sales/ingestion_20_05_2026/mart_monthly_sales.parquet'
    (FORMAT parquet, OVERWRITE true);