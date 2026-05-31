copy
    (
    /*
1.参照tpc-h数据集转换各字段类型
2.依据同一schema产生新表
3.将新表导入数据湖silver层
*/
    with new_lineitem as (select try_cast(l_orderkey as bigint)      as l_orderkey,
                                 try_cast(l_partkey as bigint)       as l_partkey,
                                 try_cast(l_suppkey as bigint)       as l_suppkey,
                                 try_cast(l_linenumber as bigint)    as l_linenumber,
                                 try_cast(l_quantity as double)      as l_quantity,
                                 try_cast(l_extendedprice as double) as l_extendedprice,
                                 try_cast(l_discount as double)      as l_discount,
                                 try_cast(l_tax as double)           as l_tax,
                                 trim(l_returnflag)                  as l_returnflag,
                                 trim(l_linestatus)                  as l_linestatus,
                                 cast(l_shipdate as date)            as l_shipdate,
                                 cast(l_commitdate as date)          as l_commitdate,
                                 cast(l_receiptdate as date)         as l_receiptdate,
                                 trim(l_shipinstruct)                as l_shipinstruct,
                                 trim(l_shipmode)                    as l_shipmode,
                                 trim(l_comment)                     as l_comment
                          from lineitem_bronzeLayer)

    select l_orderkey,
           l_partkey,
           l_suppkey,
           l_linenumber,
           l_quantity,
           l_extendedprice,
           l_discount,
           l_tax,
           l_returnflag,
           l_linestatus,
           l_shipdate,
           l_commitdate,
           l_receiptdate,
           l_shipinstruct,
           l_shipmode,
           l_comment
    from new_lineitem
    where length(l_returnflag) <= 1
      and length(l_linestatus) <= 1
      and length(l_shipinstruct) <= 25
      and length(l_shipmode) <= 10
      and length(l_comment) <= 44
    ) to 's3://silver/lineitem/ingestion_20_05_2026/lineitem.parquet'
    (FORMAT parquet, OVERWRITE true);