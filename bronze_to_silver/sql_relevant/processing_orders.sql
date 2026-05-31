copy
    (
    /*
1.参照tpc-h数据集转换各字段类型
2.依据同一schema产生新表
3.将新表导入数据湖silver层
*/
    with new_orders as (select try_cast(o_orderkey as bigint)      as o_orderkey,
                               try_cast(o_custkey as bigint)       as o_custkey,
                               trim(o_orderstatus)                 as o_orderstatus,
                               try_cast(o_totalprice as double)    as o_totalprice,
                               cast(o_orderdate as date)           as o_orderdate,
                               trim(o_orderpriority)               as o_orderpriority,
                               trim(o_clerk)                       as o_clerk,
                               try_cast(o_shippriority as integer) as o_shippriority,
                               trim(o_comment)                     as o_comment
                        from orders_bronzeLayer)

    select o_orderkey,
           o_custkey,
           o_orderstatus,
           o_totalprice,
           o_orderdate,
           o_orderpriority,
           o_clerk,
           o_shippriority,
           o_comment
    from new_orders
    where length(o_orderstatus) <= 1
      and length(o_orderpriority) <= 15
      and length(o_clerk) <= 15
      and length(o_comment) <= 79
    ) to 's3://silver/orders/ingestion_20_05_2026/orders.parquet'
    (FORMAT parquet, OVERWRITE true);