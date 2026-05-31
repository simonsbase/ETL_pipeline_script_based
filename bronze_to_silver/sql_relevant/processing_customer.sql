copy
    (
    with new_customer as (select try_cast(c_custkey as bigint)    as c_custkey,
                                 trim(c_name)                     as c_name,
                                 trim(c_address)                  as c_address,
                                 try_cast(c_nationkey as integer) as c_nationkey,
                                 trim(c_phone)                    as c_phone,
                                 try_cast(c_acctbal as double)    as c_acctbal,
                                 trim(c_mktsegment)               as c_mktsegment,
                                 trim(c_comment)                  as c_comment
                          from customer_bronzeLayer)

    select c_custkey,
           c_name,
           c_address,
           c_nationkey,
           c_phone,
           c_acctbal,
           c_mktsegment,
           c_comment
    from new_customer
    where length(c_name) <= 25
      and length(c_address) <= 40
      and length(c_phone) <= 15
      and length(c_mktsegment) <= 10
    ) to 's3://silver/customer/ingestion_20_05_2026/customer.parquet'
    (FORMAT parquet, OVERWRITE true);