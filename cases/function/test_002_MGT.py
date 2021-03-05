"""
Copyright(C), ZYTC
File name: test_002_MGT.py
Author: lixc
Version: 0.1
Date: 2021-03-01
Description: Test case for management network ports.
"""

import os
import allure
import pytest
import subprocess
from whiptail import Whiptail
from pytest_dependency import depends

board_model = os.getenv("BOARD_MODEL")
if board_model == "A8210" or board_model == "A8211" or board_model == "A8212":
    port_list = ["enP1p36s12f0", "enP1p36s12f1"]
else:
    port_list = ["enp9s0"]


@pytest.fixture(scope="module", params=port_list)
def plug_into_cable(request):
    """测试前确认网线是否插好"""
    port = request.param
    if os.getenv("MORE_INTERACTIVE"):
        w = Whiptail(width=60, height=10, title="请确认")
        w.msgbox("请确认管理网口 {} 的网线已接入千兆网络".format(port))
    return port


@allure.feature("管理网口测试")
@allure.title("查看管理网口能否正常通信")
@pytest.mark.dependency()
def test_interface_ping(plug_into_cable):
    if plug_into_cable == "enp9s0" or plug_into_cable == "enP1p36s12f0":
        dst_ip = "192.168.0.89"
    elif plug_into_cable == "enp10s0" or plug_into_cable == "enP1p36s12f1":
        dst_ip = "192.168.1.89"

    ret = subprocess.run("ping -c 3 {}".format(dst_ip), shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, universal_newlines=True, check=False)

    if ret.returncode and (plug_into_cable == "enp9s0" or plug_into_cable == "enP1p36s12f0"):
        pytest.exit("测试控制机到被测设备的网络不通，本次测试结束")

    assert 0 == ret.returncode


@allure.feature("管理网口测试")
@allure.title("查看管理网口是否被正确识别")
@pytest.mark.dependency()
def test_interface_identification(request, plug_into_cable):
    if board_model == "A8210" or board_model == "A8211" or board_model == "A8212":
        drive = "st_gmac"
    else:
        drive = "igb"

    depends(request, ["test_interface_ping[{}]".format(plug_into_cable)])
    ret = subprocess.run("ethtool -i {} | grep driver".format(plug_into_cable),
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    assert drive in ret.stdout


@allure.feature("管理网口测试")
@allure.title("查看管理网口的协商速率是否正确")
@pytest.mark.dependency()
def test_interface_stat(request, plug_into_cable):
    depends(request, ["test_interface_ping[{}]".format(plug_into_cable)])
    ret = subprocess.run("ethtool {} | grep Speed:".format(plug_into_cable),
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    assert "1000Mb/s" in ret.stdout


if __name__ == "__main__":
    pytest.main(["--alluredir", "results/MGT", "test_002_MGT.py"])
