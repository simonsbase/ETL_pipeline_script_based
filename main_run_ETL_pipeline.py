import subprocess
import sys
from pathlib import Path

scripts = ['main_bronze_to_silver.py', 'main_silver_to_gold.py']
dirs = ['bronze_to_silver', 'silver_to_gold']


def main():
    '''
    总ETl pipeline执行脚本；依次执行各层流程，并在最后将MinIO的gold层中表格导入DuckDB数据仓库，以备后续分析与可视化
    :return:None
    '''
    print()
    print('=' * 20 + ' Start Pipeline ' + '=' * 20)

    for script, s_dir in zip(scripts, dirs):
        print('Running ' + script)

        subprocess.run([sys.executable, script], cwd=Path('./' + s_dir + '/'), check=True)

        print('Ending ' + script)
        print('-' * 54)

    print('Running export_from_gold_to_warehouse.py')

    subprocess.run([sys.executable, './export_from_gold_to_warehouse.py'], check=True)

    print('Ending export_from_gold_to_warehouse.py')
    print('-' * 54)

    print('               All ETL pipelines finished!')
    print('=' * 20 + ' End Pipeline ' + '=' * 20)


if __name__ == '__main__':
    main()
