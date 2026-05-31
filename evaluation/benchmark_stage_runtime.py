import subprocess
import sys
import time
import csv

scripts = ['benchmark_bronze_to_silver.py', 'benchmark_silver_to_gold.py']
bronze_to_silver_dir = './results/bronze_to_silver.csv'
silver_to_gold_dir = './results/silver_to_gold.csv'
gold_to_warehouse_dir = './results/gold_to_warehouse.csv'


def main():
    '''
    依次执行各个阶段并计算时间
    :return:
    '''
    for script in scripts:

        start = time.perf_counter()

        subprocess.run([sys.executable, script], cwd='./', check=True)

        end = time.perf_counter()
        s_time = end - start

        if script == 'benchmark_bronze_to_silver.py':
            print('Bronze_to_silver运行时间(单位/秒)：' + str(s_time))

            with open(bronze_to_silver_dir, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([s_time])
        else:
            print('Silver_to_gold运行时间(单位/秒)：' + str(s_time))

            with open(silver_to_gold_dir, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([s_time])

    start = time.perf_counter()

    subprocess.run([sys.executable, 'export_from_gold_to_warehouse.py'], cwd='../', check=True)

    end = time.perf_counter()
    s_time = end - start
    print('Gold_to_warehouse运行时间(单位/秒)：' + str(s_time))

    with open(gold_to_warehouse_dir, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([s_time])


if __name__ == '__main__':
    main()
