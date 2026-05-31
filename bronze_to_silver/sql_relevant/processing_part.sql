copy
    (
    /*
1.参照tpc-h数据集转换各字段类型
2.依据同一schema产生新表
3.将新表导入数据湖silver层
*/
    with new_part as (select try_cast(p_partkey as bigint)     as p_partkey,
                             trim(p_name)                      as p_name,
                             trim(p_mfgr)                      as p_mfgr,
                             trim(p_brand)                     as p_brand,
                             trim(p_type)                      as p_type,
                             try_cast(p_size as integer)       as p_size,
                             trim(p_container)                 as p_container,
                             try_cast(p_retailprice as double) as p_retailprice,
                             trim(p_comment)                   as p_comment
                      from part_bronzeLayer)

    select p_partkey,
           p_name,
           p_mfgr,
           p_brand,
           p_type,
           p_size,
           p_container,
           p_retailprice,
           p_comment
    from new_part
    where length(p_name) <= 55
      and length(p_mfgr) <= 25
      and length(p_brand) <= 10
      and length(p_type) <= 25
      and length(p_container) <= 10
      and length(p_comment) <= 23

    ) to 's3://silver/part/ingestion_20_05_2026/part.parquet'
    (FORMAT parquet, OVERWRITE true);