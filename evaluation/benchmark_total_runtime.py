import subprocess
import sys
import time
import csv

scripts = ['benchmark_bronze_to_silver.py', 'benchmark_silver_to_gold.py']
total_time_dir = './results/total_time.csv'


def main():
    for script in scripts:
        subprocess.run([sys.executable, script], cwd='./', check=True)

    subprocess.run([sys.executable, 'export_from_gold_to_warehouse.py'], cwd='../', check=True)


if __name__ == '__main__':
    main_start = time.perf_counter()

    main()

    main_end = time.perf_counter()

    total_time = main_end - main_start
    print('Pipeline总体运行时间(单位/秒)：' + str(total_time))

    with open(total_time_dir, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([total_time])
