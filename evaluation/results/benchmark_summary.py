import pandas as pd

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 300)
pd.set_option('display.max_colwidth', 80)

total_time_dir = './total_time.csv'
bronze_to_silver_dir = './bronze_to_silver.csv'
silver_to_gold_dir = './silver_to_gold.csv'
gold_to_warehouse_dir = './gold_to_warehouse.csv'
tables_bronze_to_silver_dir = './tables_bronze_to_silver.csv'
tables_silver_to_gold_dir = './tables_silver_to_gold.csv'


def total_time_avg():
    total_time = pd.read_csv(total_time_dir, header=None)
    total_time.columns = ['Runtime']
    total_time.index = ['Warmup'] + [f'第{i}次' for i in range(1, len(total_time))]

    # print(total_time)
    total_time.to_csv(total_time_dir, header=False)

    avg = total_time.loc[total_time.index != 'Warmup']['Runtime'].mean()
    # print(avg)

    avg_row = pd.DataFrame({'Runtime': [avg]}, index=['后5次平均值'])
    total_time_summary = pd.concat([total_time, avg_row])
    # print(total_time_summary)

    total_time_summary.to_csv(total_time_dir, header=False)


def bronze_to_silver_time_avg():
    bronze_to_silver_time = pd.read_csv(bronze_to_silver_dir, header=None)
    bronze_to_silver_time.columns = ['Runtime']
    bronze_to_silver_time.index = ['Warmup'] + [f'第{i}次' for i in range(1, len(bronze_to_silver_time))]

    # print(bronze_to_silver_time)
    bronze_to_silver_time.to_csv(bronze_to_silver_dir, header=False)

    avg = bronze_to_silver_time.loc[bronze_to_silver_time.index != 'Warmup']['Runtime'].mean()
    # print(avg)

    avg_row = pd.DataFrame({'Runtime': [avg]}, index=['后5次平均值'])
    bronze_to_silver_time_summary = pd.concat([bronze_to_silver_time, avg_row])
    # print(bronze_to_silver_time_summary)

    bronze_to_silver_time_summary.to_csv(bronze_to_silver_dir, header=False)


def silver_to_gold_avg():
    silver_to_gold_time = pd.read_csv(silver_to_gold_dir, header=None)
    silver_to_gold_time.columns = ['Runtime']
    silver_to_gold_time.index = ['Warmup'] + [f'第{i}次' for i in range(1, len(silver_to_gold_time))]

    # print(silver_to_gold_time)
    silver_to_gold_time.to_csv(silver_to_gold_dir, header=False)

    avg = silver_to_gold_time.loc[silver_to_gold_time.index != 'Warmup']['Runtime'].mean()
    # print(avg)

    avg_row = pd.DataFrame({'Runtime': [avg]}, index=['后5次平均值'])
    silver_to_gold_time_summary = pd.concat([silver_to_gold_time, avg_row])
    # print(silver_to_gold_time_summary)

    silver_to_gold_time_summary.to_csv(silver_to_gold_dir, header=False)


def gold_to_warehouse_avg():
    gold_to_warehouse_time = pd.read_csv(gold_to_warehouse_dir, header=None)
    gold_to_warehouse_time.columns = ['Runtime']
    gold_to_warehouse_time.index = ['Warmup'] + [f'第{i}次' for i in range(1, len(gold_to_warehouse_time))]

    # print(gold_to_warehouse_time)
    gold_to_warehouse_time.to_csv(gold_to_warehouse_dir, header=False)

    avg = gold_to_warehouse_time.loc[gold_to_warehouse_time.index != 'Warmup']['Runtime'].mean()
    # print(avg)

    avg_row = pd.DataFrame({'Runtime': [avg]}, index=['后5次平均值'])
    gold_to_warehouse_time_summary = pd.concat([gold_to_warehouse_time, avg_row])
    # print(gold_to_warehouse_time_summary)

    gold_to_warehouse_time_summary.to_csv(gold_to_warehouse_dir, header=False)


def tables_bronze_to_silver_avg():
    tables_bronze_to_silver = pd.read_csv(tables_bronze_to_silver_dir, header=None,
                                          names=['Script', 'Runtime', 'Line/s'])
    # print(tables_bronze_to_silver)

    tables_bronze_to_silver['temp_index'] = tables_bronze_to_silver.groupby('Script').cumcount()

    runtime_wide = tables_bronze_to_silver.pivot(index='temp_index', columns='Script', values='Runtime')
    # print(runtime_wide)

    line_wide = tables_bronze_to_silver.pivot(index='temp_index', columns='Script', values='Line/s')
    # print(line_wide)

    labels = ['Warmup'] + [f'第{i}次' for i in range(1, len(runtime_wide))]

    runtime_wide.index = [f'{label}（Runtime）' for label in labels]
    line_wide.index = [f'{label}（Line/s）' for label in labels]

    tables_bronze_to_silver_summary = pd.concat([runtime_wide, line_wide])
    # print(tables_bronze_to_silver_summary)

    tables_bronze_to_silver_summary.loc['后5次平均值（Runtime）'] = tables_bronze_to_silver_summary.loc[
        [f'第{i}次（Runtime）' for i in range(1, len(runtime_wide))]].mean()
    # print(tables_bronze_to_silver_summary)

    tables_bronze_to_silver_summary.loc['后5次平均值（Line/s）'] = tables_bronze_to_silver_summary.loc[
        [f'第{i}次（Line/s）' for i in range(1, len(line_wide))]].mean()

    # print(tables_bronze_to_silver_summary)
    tables_bronze_to_silver_summary.to_csv(tables_bronze_to_silver_dir)


def tables_silver_to_gold_avg():
    tables_silver_to_gold = pd.read_csv(tables_silver_to_gold_dir, header=None, names=['Script', 'Runtime', 'Line/s'])
    # print(tables_silver_to_gold)

    tables_silver_to_gold['temp_index'] = tables_silver_to_gold.groupby('Script').cumcount()

    runtime_wide = tables_silver_to_gold.pivot(index='temp_index', columns='Script', values='Runtime')
    # print(runtime_wide)

    line_wide = tables_silver_to_gold.pivot(index='temp_index', columns='Script', values='Line/s')
    # print(line_wide)

    labels = ['Warmup'] + [f'第{i}次' for i in range(1, len(runtime_wide))]

    runtime_wide.index = [f'{label}（Runtime）' for label in labels]
    line_wide.index = [f'{label}（Line/s）' for label in labels]

    tables_silver_to_gold_summary = pd.concat([runtime_wide, line_wide])
    # print(tables_silver_to_gold_summary)

    tables_silver_to_gold_summary.loc['后5次平均值（Runtime）'] = tables_silver_to_gold_summary.loc[
        [f'第{i}次（Runtime）' for i in range(1, len(runtime_wide))]].mean()
    # print(tables_silver_to_gold_summary)

    tables_silver_to_gold_summary.loc['后5次平均值（Line/s）'] = tables_silver_to_gold_summary.loc[
        [f'第{i}次（Line/s）' for i in range(1, len(line_wide))]].mean()

    # print(tables_silver_to_gold_summary)
    tables_silver_to_gold_summary.to_csv(tables_silver_to_gold_dir)


def main():
    total_time_avg()

    bronze_to_silver_time_avg()
    silver_to_gold_avg()
    gold_to_warehouse_avg()

    tables_bronze_to_silver_avg()
    tables_silver_to_gold_avg()


if __name__ == '__main__':
    main()
