
import psutil
import subprocess
from loguru import logger


# define path of log file
LOG_FILE_PATH = "./logs"

logger.add(LOG_FILE_PATH)

# get available memory size
mem = psutil.virtual_memory()

mem_available = mem.available

test_mem_size = int(mem_available * 0.01)

# run memory test
ret = subprocess.run("memtester {}B 1".format(test_mem_size), shell=True, check=True)

# pass or fail
if ret.returncode != 0:
    logger.error("memtester 内存测试失败！")
else:
    logger.info("memtester 内存测试通过！")

