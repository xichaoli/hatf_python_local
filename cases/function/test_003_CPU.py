"""
Copyright(C), ZYTC
File name: test_003_CPU.py
Author: lixc
Version: 0.2
Date: 2021-03-03
Description: Test case for CPU status.
"""

import os
import allure
import pytest
import psutil
import subprocess


board_model = os.getenv("BOARD_MODEL")
if board_model == "N4210":
    cpu_num = 4
    cpu_freq = 1400.00
else:
    cpu_num = 4
    cpu_freq = 1600.00


@allure.feature("CPU状态测试")
@allure.title("查看CPU核心数量是否正确")
def test_cpu_num():
    assert cpu_num == psutil.cpu_count()

@allure.feature("CPU状态测试")
@allure.title("查看是否有CPU核心离线")
def test_cpu_offline():
    ret = subprocess.run("lscpu", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    assert "Off-line" not in ret.stdout, "有CPU核心离线，请使用 lscpu -e -c 做进一步检测"


@allure.feature("CPU状态测试")
@allure.title("查看CPU主频是否正确")
def test_cpu_freq():
    assert cpu_freq == psutil.cpu_freq().current


if __name__ == "__main__":
    pytest.main(["--alluredir", "results/CPU", "test_003_CPU.py"])

