from dotenv import load_dotenv
import sys
import my_journalist
import os
import subprocess
import logging
from my_journalist.utils.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

load_dotenv()

# alembic.ini 的路徑
CONFIG_PATH: str = os.path.join(os.path.dirname(my_journalist.__file__), 'alembic.ini')
# migration script 的路徑
ALEMBIC_SCRIPT_LOCATION = os.path.dirname(__file__)

def update_script_location():
    sed_command = f"sed -i 's|script_location = .*|script_location = {ALEMBIC_SCRIPT_LOCATION}|g' {CONFIG_PATH}"
    try:
        subprocess.run(sed_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error updating script location: {e}", file=sys.stderr)
        sys.exit(1)

def run_alembic(args):
    print(f"Running command: alembic -c {CONFIG_PATH} {' '.join(args)}")
    try:
        result = subprocess.run(['alembic', '-c', CONFIG_PATH] + args, check=True, text=True, capture_output=True)
        print(result.stdout)  # 打印標準輸出
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running Alembic: {e.stderr}", file=sys.stderr)  # 打印錯誤信息
        return e.returncode

if __name__ == '__main__':
    # 取得 command line 的參數
    args = sys.argv[1:]  # 直接獲取參數列表
    update_script_location()
    return_code = run_alembic(args)
    sys.exit(return_code)


