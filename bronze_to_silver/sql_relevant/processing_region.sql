copy
    (
    /*
1.参照tpc-h数据集转换各字段类型
2.依据同一schema产生新表
3.将新表导入数据湖silver层
*/
    with new_region as (select try_cast(r_regionkey as integer) as r_regionkey,
                               trim(r_name)                     as r_name,
                               trim(r_comment)                  as r_comment
                        from region_bronzeLayer)

    select r_regionkey, r_name, r_comment
    from new_region
    where length(r_name) <= 55
      and length(r_comment) <= 152
    )
    to 's3://silver/region/ingestion_20_05_2026/region.parquet'
    (format parquet, overwrite true);