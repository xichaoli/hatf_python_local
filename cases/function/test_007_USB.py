"""
Copyright(C), ZYTC
File name: test_001_USB.py
Author: lixc
Version: 0.2
Date: 2021-03-03
Description: Test case for USB ports.
"""

import os
import allure
import pytest
import subprocess
from whiptail import Whiptail
from pytest_dependency import depends

board_model = os.getenv("BOARD_MODEL")
if board_model == "A8210" or board_model == "A8245":
    device_list = ["0951:1665", "046d:c534"]
else: # A8240
    device_list = ["090c:1000", "046d:c534", "0781:5590"]


@pytest.fixture(scope="module", params=device_list)
def plug_into_usb(request):
    """测试前确认所需设备是否插好"""
    """其中Samsung U盘插在竖立的USB3.0口"""
    device_vendor = request.param

    if os.getenv("MORE_INTERACTIVE"):
         w = Whiptail(width=60, height=10, title="需确认")

         if device_vendor == "046d:c534":
             device = "Logitech 无线键鼠接收器"
         elif device_vendor == "0781:5590":
             device = "SanDisk U盘"
         elif device_vendor == "090c:1000":
             device = "Samsung U盘"
         else:
             device = "其它"

         w.msgbox("请确认测试用USB设备 {} 已正确插入".format(device))

    return device_vendor


@allure.feature("USB端口测试")
@allure.title("查看U盘是否被正确识别")
@pytest.mark.dependency()
@pytest.mark.skipif(board_model=="A8211" or board_model=="A8212" or board_model=="A8246", reason="此型号产品没有使用USB口")
def test_usb_identification(plug_into_usb):
    ret = subprocess.run("lsusb -d {}".format(plug_into_usb),
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    assert 0 == ret.returncode


@allure.feature("USB端口测试")
@allure.title("查看USB接口所遵循的协议版本号是否为预期")
@pytest.mark.dependency()
def test_usb_protocol(request, plug_into_usb):
    depends(request, ["test_usb_identification[{}]".format(plug_into_usb)])
    ret = subprocess.run("lsusb -d {} -v | grep bcdUSB".format(plug_into_usb),
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    assert "2.00" in ret.stdout or "2.10" in ret.stdout or "3.00" in ret.stdout or "3.10" in ret.stdout or "3.20" in ret.stdout


if __name__ == "__main__":
    pytest.main(["--alluredir", "results/USB", "test_007_USB.py"])
