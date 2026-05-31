import duckdb
from config.configuration import config_minio


def create_connection():
    '''
    从脚本中连接DuckDB数据库并执行预先配置
    :return: DuckDB调用接口，便于后续利用DuckDB sql引擎执行sql文件
    '''
    connection = duckdb.connect()
    connection.execute(config_minio)

    return connection


def run_sql(connection, sql_path):
    '''
    读取sql代码并执行
    :param connection:DuckDB sql引擎接口
    :param sql_path:要被执行的sql文件位置
    :return: None
    '''
    sql = sql_path.read_text()
    connection.execute(sql)


def run_sql_job(sql_path, registered_table_name=None, registered_table=None):
    '''
    用于执行bronze层到silver层以及silver层到gold层的sql作业
    :param sql_path:要被执行的sql文件位置
    :param registered_table_name:bronze层到silver层pipeline参数，用于向DuckDB注册表
    :param registered_table:bronze层到silver层pipeline参数，用于向DuckDB注册表
    :return:DuckDB sql引擎接口
    '''
    connection = create_connection()

    if (registered_table_name is None) != (registered_table is None):
        raise ValueError('Both registered_table_name and registered_table have to be passed all together!')

    # 如果两个参数都不为空，则说明此时处于bronze层到silver层的处理之中
    if registered_table_name is not None and registered_table is not None:
        connection.register(registered_table_name, registered_table)

    run_sql(connection, sql_path)
    return connection


def view_table(connection, parquet_path, limit=20):
    '''
    查看表；用于在各层流程处理完后检查是否处理成功
    :param connection: DuckDB sql引擎接口
    :param parquet_path:Gold层中parquet文件位置
    :param limit:查询数量
    :return:
    '''
    return connection.execute(f'''select * from read_parquet('{parquet_path}') limit {limit}''').df()
