copy (
     /*
     1.从silver读入相关表
     2.构造sales事实表并构造额外字段例如各明细项上缴税费等
     3.将该表导入gold层
    */
    with lineitem as (select *
                      from read_parquet('s3://silver/lineitem/ingestion_20_05_2026/lineitem.parquet')),

         orders as (select *
                    from read_parquet('s3://silver/orders/ingestion_20_05_2026/orders.parquet')),

         fact_sales as (select *
                        from orders
                                 join lineitem on o_orderkey = l_orderkey)

    select o_orderkey,
           l_linenumber,
           o_custkey,
           l_partkey,
           l_suppkey,
           o_orderdate,
           l_shipdate,
           l_commitdate,
           l_receiptdate,
           o_orderstatus,
           l_returnflag,
           l_linestatus,
           l_shipmode,
           l_quantity,
           l_extendedprice,
           l_discount,
           l_tax,
           l_extendedprice * (1 - l_discount)               as discount_price,
           l_extendedprice * l_discount                     as discount_amount,
           l_extendedprice * (1 - l_discount) * l_tax       as tax_amount,
           l_extendedprice * (1 - l_discount) * (1 + l_tax) as plus_tax_price
    from fact_sales
    )
    to 's3://gold/fact_sales/ingestion_20_05_2026/fact_sales.parquet'
    (FORMAT parquet, OVERWRITE true);