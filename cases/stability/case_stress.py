"""
Copyright(C), ZYTC
File name: case_stress.py
Author: lixc
Version: 0.1
Date: 2021-03-05
Description: Load and stress a computer system .
"""
import os
import time
import subprocess
from loguru import logger
from whiptail import Whiptail


# define path of log file
time_now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
logs_top_dir = os.getenv("LOGS_DIR")
LOG_FILE_PATH = logs_top_dir + "/stress_test_" + time_now

logger.add(LOG_FILE_PATH)

w = Whiptail(width=50, height=8)

test_cpu_num = w.inputbox("请输入测试 CPU 使用的进程数：", default="8")[0]
test_io_num =  w.inputbox("请输入测试 IO 使用的进程数：", default="8")[0]
test_vm_num =  w.inputbox("请输入测试 内存 使用的进程数：", default="8")[0]
test_hdd_num = w.inputbox("请输入测试 磁盘 使用的进程数：", default="8")[0]
test_timeout = w.inputbox("请输入测试持续时间：(s,m,h,d)", default="8h")[0]

# run test
ret = subprocess.run("stress --cpu {} --io {} --vm {} --hdd {} --timeout {}".format(test_cpu_num, test_io_num, test_vm_num, test_hdd_num, test_timeout), \
        shell=True, check=True)

# pass or fail
if ret.returncode != 0:
    logger.error("stress 压力测试失败！")
else:
    logger.info("stress 压力测试通过！")

