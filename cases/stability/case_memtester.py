"""
Copyright(C), ZYTC
File name: case_memtester.py
Author: lixc
Version: 0.1
Date: 2021-03-05
Description: Testing the memory subsystem for faults.
"""
import os
import time
import psutil
import subprocess
from loguru import logger
from whiptail import Whiptail


# define path of log file
time_now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
logs_top_dir = os.getenv("LOGS_DIR")
LOG_FILE_PATH = logs_top_dir + "/memory_test_" + time_now

logger.add(LOG_FILE_PATH)

# get available memory size
mem = psutil.virtual_memory()

mem_available = mem.available

w = Whiptail(width=50, height=8)

test_rate = w.inputbox("请输入测试内存比率:", default="0.9")[0]

test_mem_size = int(mem_available * float(test_rate))

test_round_num = w.inputbox("请输入内存测试轮数:", default="3")[0]

# run memory test
ret = subprocess.run("memtester {}B {}".format(test_mem_size, test_round_num), shell=True, check=True)

# pass or fail
if ret.returncode != 0:
    logger.error("memtester 内存测试失败！")
else:
    logger.info("memtester 内存测试通过！")

