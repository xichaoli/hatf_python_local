"""
Copyright(C), ZYTC
File name: test_006_beep.py
Author: lixc
Version: 0.2
Date: 2021-03-02
Description: Test case for beep.
"""

import os
import allure
import pytest
import subprocess
from whiptail import Whiptail


@allure.feature("蜂鸣器测试")
@allure.title("查看能否控制蜂鸣器出声")
def test_beep_up():
    subprocess.run("i2cset -f -y 3 0x64 0x8 0xf9", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    w = Whiptail(width=40, height=10, title="请确认")
    ret = w.yesno("您是否听到了蜂鸣音？", default="no")
    """
    感觉yesno这里有bug，没有default参数，不显示box；
    有了default参数后，选yes返还False，选no返回True
    所以下面的assert 多加了一个 not
    """
    assert not ret, "不能听到蜂鸣音，请做进一步检查"


@allure.feature("蜂鸣器测试")
@allure.title("查看能否控制蜂鸣器关闭")
def test_beep_down():
    ret = subprocess.run("i2cset -f -y 3 0x64 0x8 0xf8", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    assert 0 == ret.returncode

if __name__ == "__main__":
    pytest.main(["--alluredir", "results/RTC", "test_006_beep.py"])
