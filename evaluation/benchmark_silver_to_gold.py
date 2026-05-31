import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STAGE_DIR = PROJECT_ROOT / 'silver_to_gold'

scripts = ['processing_dim_customer.py', 'processing_dim_nation.py', 'processing_dim_part.py',
           'processing_dim_partsupp.py', 'processing_dim_region.py', 'processing_dim_supplier.py',
           'processing_fact_sales.py', 'processing_mart_monthly_sales.py', 'processing_mart_product_performance.py',
           'processing_mart_sales_each_region.py', 'processing_mart_supplier_performance.py']

for script in scripts:
    subprocess.run([sys.executable, 'processing_tables/' + script], cwd=STAGE_DIR, check=True)
