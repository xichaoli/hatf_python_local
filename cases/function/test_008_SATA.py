"""
Copyright(C), ZYTC
File name: test_001_USB.py
Author: lixc
Version: 0.2
Date: 2021-03-03
Description: Test case for SATA ports.
"""

import os
import allure
import pytest
import subprocess
from whiptail import Whiptail

board_model = os.getenv("BOARD_MODEL")
if board_model == "A8240":
    #disk_model = ["WD1004FBYZ-23YC", "ST1000VX005-2EZ1", "DGDZM256S3DMASD"]
    disk_model = ["ST1000VX005-2EZ1", "ST4000VX007-2DT1"]
elif board_model == "A8246":
    disk_model = ["WD1004FBYZ-23YC"]
elif board_model == "A8212":
    disk_model = ["GG46T256S3C27"]
else:
    disk_model = ["ST4000VX007-2DT1", "ST1000VX005-2EZ1"]

@pytest.fixture(scope="module", params=disk_model)
def plug_into_harddisk(request):
    """测试前确认所需设备是否插好"""
    model = request.param
    if os.getenv("MORE_INTERACTIVE"):
        w = Whiptail(width=60, height=10, title="需确认")
        w.msgbox("请确认设备型号为 {} 的测试硬盘已插入SATA口。".format(model))
    return model


@allure.feature("SATA 端口测试")
@allure.title("查看SATA口硬盘是否被正确识别")
@pytest.mark.skipif(board_model=="A8211" or board_model=="A82451", reason="此型号产品没有使用SATA口")
def test_sata_identification(plug_into_harddisk):
    ret = subprocess.run("lsscsi", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    assert plug_into_harddisk in ret.stdout, "硬盘{}没有被正确识别".format(plug_into_harddisk)


if __name__ == "__main__":
    pytest.main(["--alluredir", "results/SATA", "test_008_SATA.py"])
