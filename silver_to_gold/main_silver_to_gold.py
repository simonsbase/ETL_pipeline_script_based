import subprocess
import sys
from pathlib import Path

scripts = ['processing_dim_customer.py', 'processing_dim_nation.py', 'processing_dim_part.py',
           'processing_dim_partsupp.py', 'processing_dim_region.py', 'processing_dim_supplier.py',
           'processing_fact_sales.py', 'processing_mart_monthly_sales.py', 'processing_mart_product_performance.py',
           'processing_mart_sales_each_region.py', 'processing_mart_supplier_performance.py']
'''
Note: Silver层到gold层的脚本执行由于指标表与事实表的依赖关系而产生依赖性，
对应四个指标表的脚本必须在sales事实表构造完成并导入dold层以后才能执行
'''
for script in scripts:
    py_script_dir = Path('./processing_tables/' + script)

    print('     Running ' + script)

    subprocess.run([sys.executable, py_script_dir], check=True)

    print('     Ending ' + script)
    print()

print('All scripts of silver_to_gold finished!')
