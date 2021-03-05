"""
Copyright(C), ZYTC
File name: test_001_cpu.py
Author: lixc
Version: 0.2
Date: 2021-03-03
Description: Test case for memory status.
"""

import os
import allure
import pytest
import psutil
import subprocess


board_model = os.getenv("BOARD_MODEL")

if board_model == "N4210":
    memsize = 16
elif board_model == "A82451":
    memsize = 64
else:
    memsize = 32


@allure.feature("内存状态测试")
@allure.title("查看内存容量是否正确")
def test_mem_size():
    assert memsize == psutil.virtual_memory().total // 1000000000

if __name__ == "__main__":
    pytest.main(["--alluredir", "results/MEM", "test_004_MEM.py"])
