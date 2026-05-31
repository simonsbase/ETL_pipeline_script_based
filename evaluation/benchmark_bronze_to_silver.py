import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STAGE_DIR = PROJECT_ROOT / 'bronze_to_silver'

scripts = ['processing_region.py', 'processing_nation.py', 'processing_supplier.py', 'processing_customer.py',
           'processing_part.py', 'processing_partsupp.py', 'processing_orders.py', 'processing_lineitem.py']

# 遍历所有脚本，依次执行
for script in scripts:
    subprocess.run([sys.executable, 'processing_tables/' + script], cwd=STAGE_DIR, check=True)
