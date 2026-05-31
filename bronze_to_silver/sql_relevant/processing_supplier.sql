copy
(
/*
1.参照tpc-h数据集转换各字段类型
2.依据同一schema产生新表
3.将新表导入数据湖silver层
*/
    with new_supplier as (select try_cast(s_suppkey as bigint)    as s_suppkey,
                                 trim(s_name)                     as s_name,
                                 trim(s_address)                  as s_address,
                                 try_cast(s_nationkey as integer) as s_nationkey,
                                 trim(s_phone)                    as s_phone,
                                 try_cast(s_acctbal as double)    as s_acctbal,
                                 trim(s_comment)                  as s_comment
                          from supplier_bronzeLayer)

    select s_suppkey, s_name, s_address, s_nationkey, s_phone, s_acctbal, s_comment
    from new_supplier
    where length(s_name) <= 25
      and length(s_comment) <= 101
      and length(s_address) <= 40
      and length(s_phone) <= 15

    ) to 's3://silver/supplier/ingestion_20_05_2026/supplier.parquet'
    (FORMAT parquet, OVERWRITE true);