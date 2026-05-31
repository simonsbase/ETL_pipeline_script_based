copy
    (
    /*
1.参照tpc-h数据集转换各字段类型
2.依据同一schema产生新表
3.将新表导入数据湖silver层
*/
    with new_nation as (select try_cast(n_nationkey as integer) as n_nationkey,
                               trim(n_name)                     as n_name,
                               try_cast(n_regionkey as integer) as n_regionkey,
                               trim(n_comment)                  as n_comment
                        from nation_bronzeLayer)

    select n_nationkey, n_name, n_regionkey, n_comment
    from new_nation
    where length(n_name) <= 25
      and length(n_comment) <= 152

    ) to 's3://silver/nation/ingestion_20_05_2026/nation.parquet'
    (FORMAT parquet, OVERWRITE true);