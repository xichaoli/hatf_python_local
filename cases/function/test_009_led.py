"""
Copyright(C), ZYTC
File name: test_009_led.py
Author: lixc
Version: 0.2
Date: 2020-11-13
Description: Test case for led.
"""

import os
import time
import allure
import pytest
import subprocess
from whiptail import Whiptail

board_model = os.getenv("BOARD_MODEL")

@allure.feature("管理板 SYS LED灯测试")
@allure.title("查看能否控制LED灯 绿色长亮")
@pytest.mark.skipif(board_model!="A8210" and board_model!="A8240", reason="此型号产品没有使用管理板的可控LED灯")
def test_led_up_green():
    if board_model == "A8210":
        subprocess.run("echo 255 > /sys/bus/i2c/devices/0-0062/leds/pca955x:0/brightness",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    else: # A8240
        subprocess.run("i2cset -f -y 3 0x64 0xc 0x01", shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    w = Whiptail(width=40, height=10, title="请确认")
    ret = w.yesno("请确认LED灯状态是否为 绿色长亮？", default="no")
    assert not ret, "LED灯状态不是 绿色长亮，请做进一步检查"


@allure.feature("管理板 SYS LED灯测试")
@allure.title("查看能否控制LED灯 绿色闪烁")
@pytest.mark.skipif(board_model!="A8210" and board_model!="A8240", reason="此型号产品没有使用管理板的可控LED灯")
def test_led_blink_green():
    if board_model == "A8210":
        subprocess.run("echo 127 > /sys/bus/i2c/devices/0-0062/leds/pca955x:0/brightness",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    else: #A8240
        subprocess.run("i2cset -f -y 3 0x64 0xc 0x11", shell=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    w = Whiptail(width=40, height=10, title="请确认")

    if os.getenv("MORE_INTERACTIVE"):
        ret = w.yesno("请确认LED灯状态是否为 绿色闪烁？A8210 由于驱动原因，闪烁频率很快。", default="no")
        assert not ret, "LED灯状态不是 绿色闪烁，请做进一步检查"
    else:
        ret = w.yesno("请确认LED灯状态是否为 绿色闪烁？A8210 由于驱动原因，闪烁频率很快。", default="yes")
        time.sleep(3)
        assert ret, "LED灯状态不是 绿色闪烁，请做进一步检查"



@allure.feature("管理板 SYS LED灯测试")
@allure.title("查看能否控制LED灯 红色长亮")
@pytest.mark.skipif(board_model!="A8210" and board_model!="A8240", reason="此型号产品没有使用管理板的可控LED灯")
def test_led_up_red():
    if board_model == "A8210":
        subprocess.run("echo 255 > /sys/bus/i2c/devices/0-0062/leds/pca955x:1/brightness",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    else: #A8240
        subprocess.run("i2cset -f -y 3 0x64 0xc 0x12", shell=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    w = Whiptail(width=40, height=10, title="请确认")
    if os.getenv("MORE_INTERACTIVE"):
        ret = w.yesno("请确认LED灯状态是否为 红色长亮？", default="no")
        assert not ret, "LED灯状态不是 红色长亮，请做进一步检查"
    else:
        ret = w.yesno("请确认LED灯状态是否为 红色长亮？", default="yes")
        time.sleep(3)
        assert ret, "LED灯状态不是 红色长亮，请做进一步检查"


@allure.feature("管理板 SYS LED灯测试")
@allure.title("查看能否控制LED灯 红色闪烁")
@pytest.mark.skipif(board_model!="A8210" and board_model!="A8240", reason="此型号产品没有使用管理板的可控LED灯")
def test_led_blink_red():
    if board_model == "A8210":
        subprocess.run("echo 127 > /sys/bus/i2c/devices/0-0062/leds/pca955x:1/brightness",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    else: #A8240
        subprocess.run("i2cset -f -y 3 0x64 0xc 0x22", shell=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    w = Whiptail(width=40, height=10, title="请确认")
    if os.getenv("MORE_INTERACTIVE"):
        ret = w.yesno("请确认LED灯状态是否为 红色闪烁？A8210 由于驱动原因，闪烁频率很快。", default="no")
        assert not ret, "LED灯状态不是 红色闪烁，请做进一步检查"
    else:
        ret = w.yesno("请确认LED灯状态是否为 红色闪烁？A8210 由于驱动原因，闪烁频率很快。", default="yes")
        time.sleep(3)
        assert ret, "LED灯状态不是 红色闪烁，请做进一步检查"


@allure.feature("管理板 SYS LED灯测试")
@allure.title("查看能否控制LED灯灭")
@pytest.mark.skipif(board_model!="A8210" and board_model!="A8240", reason="此型号产品没有使用管理板的可控LED灯")
def test_led_down():
    if board_model == "A8210":
        with allure.step("熄灭绿色灯"):
            subprocess.run("echo 0 > /sys/bus/i2c/devices/0-0062/leds/pca955x:0/brightness",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        with allure.step("熄灭红色灯"):
            subprocess.run("echo 0 > /sys/bus/i2c/devices/0-0062/leds/pca955x:1/brightness",
                       shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    else: # A8240
        subprocess.run("i2cset -f -y 3 0x64 0xc 0x0", shell=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    w = Whiptail(width=40, height=10, title="请确认")
    if os.getenv("MORE_INTERACTIVE"):
        ret = w.yesno("请确认LED灯状态是否为灭？", default="no")
        assert not ret, "LED灯状态不是灭，请做进一步检查"
    else:
        ret = w.yesno("请确认LED灯状态是否为灭？", default="yes")
        time.sleep(2)
        assert ret, "LED灯状态不是灭，请做进一步检查"


if __name__ == "__main__":
    pytest.main(["--alluredir", "results/led", "test_009_led.py"])
