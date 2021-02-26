
import subprocess
from loguru import logger

# define path of log file
LOG_FILE_PATH = "./logs"

logger.add(LOG_FILE_PATH)

# run test
ret = subprocess.run("stress --cpu 8 --io 4 --vm 4 --hdd 4 --timeout 120s", shell=True, check=True)

# pass or fail
if ret.returncode != 0:
    logger.error("stress 压力测试失败！")
else:
    logger.info("stress 压力测试通过！")

