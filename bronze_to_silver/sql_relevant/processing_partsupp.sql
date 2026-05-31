copy
    (
    /*
1.参照tpc-h数据集转换各字段类型
2.依据同一schema产生新表
3.将新表导入数据湖silver层
*/
    with new_partsupp as (select try_cast(ps_partkey as bigint)    as ps_partkey,
                                 try_cast(ps_suppkey as bigint)    as ps_suppkey,
                                 try_cast(ps_availqty as bigint)   as ps_availqty,
                                 try_cast(ps_supplycost as double) as ps_supplycost,
                                 trim(ps_comment)                  as ps_comment
                          from partsupp_bronzeLayer)

    select ps_partkey, ps_suppkey, ps_availqty, ps_supplycost, ps_comment
    from new_partsupp

    where length(ps_comment) <= 199

    ) to 's3://silver/partsupp/ingestion_20_05_2026/partsupp.parquet'
    (FORMAT parquet, OVERWRITE true);