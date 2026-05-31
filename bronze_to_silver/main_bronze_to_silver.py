import subprocess
import sys
from pathlib import Path

scripts = ['processing_region.py', 'processing_nation.py', 'processing_supplier.py', 'processing_customer.py',
           'processing_part.py', 'processing_partsupp.py', 'processing_orders.py', 'processing_lineitem.py']

# 遍历所有脚本，依次执行
for script in scripts:
    py_script_dir = Path('./processing_tables/' + script)

    print('     Running ' + script)

    subprocess.run([sys.executable, py_script_dir], check=True)

    print('     Ending ' + script)
    print()

print('All scripts of bronze_to_silver finished!')
