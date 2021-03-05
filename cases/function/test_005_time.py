"""
Copyright(C), ZYTC
File name: test_005_time.py
Author: lixc
Version: 0.2
Date: 2021-03-02
Description: Test case for time set.
Preset : 设备可以连通互联网或其它内网ntp服务器
"""

import os
import allure
import pytest
import subprocess

@allure.feature("时间测试")
@allure.title("从ntp服务器同步时间")
def test_time_sync():
    ret = subprocess.run("ntpdate -u 192.168.0.89", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    assert 0 == ret.returncode


@allure.feature("时间测试")
@allure.title("查看rtc设备是否能正确写入")
@pytest.mark.repeat(2)
def test_rtc_write():
    ret = subprocess.run("hwclock -w", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    assert 0 == ret.returncode


@allure.feature("时间测试")
@allure.title("查看rtc设备是否能正确读取")
def test_rtc_read():
    ret = subprocess.run("hwclock -r", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    assert 0 == ret.returncode

if __name__ == "__main__":
    pytest.main(["--alluredir", "results/RTC", "test_005_rtc.py"])
