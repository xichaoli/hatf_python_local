"""
Copyright(C), ZYTC
File name: test_001_start.py
Author: lixc
Version: 0.1
Date: 2021-03-01
Description: Determines whether the system started successfully.
"""

import os
import allure
import pytest
from whiptail import Whiptail

@allure.feature("查看系统是否正常启动")
@allure.title("查看显示器输出，确认系统启动状态")
@pytest.mark.dependency()
def test_monitor():
    w = Whiptail(width=60, height=10)
    if os.getenv("MORE_INTERACTIVE"):
        ret = w.yesno("请查看显示器输出，确认系统是否启动成功", default="no")
        if ret:
            pytest.exit("系统启动失败，本次测试结束")
        assert not ret, "通过显示器观察，系统启动未成功"
    else:
        ret = w.yesno("请查看显示器输出，确认系统是否启动成功", default="yes")
        if not ret:
            pytest.exit("系统启动失败，本次测试结束")
        assert ret, "通过显示器观察，系统启动未成功"


@allure.feature("查看系统是否正常启动")
@allure.title("查看串口终端输出，确认系统启动状态")
class TestSerial:
    @pytest.mark.dependency(depends=["test_monitor"])
    def test_serial_output(self):
        w = Whiptail(width=60, height=10)
        if os.getenv("MORE_INTERACTIVE"):
            ret = w.yesno("请查看串口终端输出，确认系统是否启动成功", default="no")
            assert not ret, "通过串口终端观察，系统启动未成功"
        else:
            ret = w.yesno("请查看串口终端输出，确认系统是否启动成功", default="yes")
            assert ret, "通过串口终端观察，系统启动未成功"

    @pytest.mark.dependency(depends=["TestSerial::test_serial_output"])
    def test_serial_input(self):
        w = Whiptail(width=60, height=10)
        if os.getenv("MORE_INTERACTIVE"):
            ret = w.yesno("请串口终端输入字符，确认串口终端是否可以正确输入字符", default="no")
            assert not ret, "串口终端不能正确输入字符"
        else:
            ret = w.yesno("请串口终端输入字符，确认串口终端是否可以正确输入字符", default="yes")
            assert ret, "串口终端不能正确输入字符"

if __name__ == "__main__":
    pytest.main(["--alluredir", "results/start", "test_001_start.py"])
