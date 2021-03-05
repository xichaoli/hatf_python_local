# entry
import os
import pytest
import subprocess
from loguru import logger
from whiptail import Whiptail


w = Whiptail(width=50, height=12)

if os.getenv("MORE_INTERACTIVE"):
    w.title = "Welcome"
    w.height = 8
    w.msgbox("欢迎使用自动检测系统，请点击 '确认' 开始测试。")
    w.title = "主板型号"
    w.height = 15
    board_model = w.radiolist("请选择主板型号：", (\
        "A8210        三扩主板", \
        "A8211        堡垒机", \
        "A8212        绿盟防火墙", \
        "A8240        四扩主板", \
        "A8245        5.0主板", \
        "A82451       5.0整机", \
        "A8246        619整机"))[0][0]
        
    w.title = "主板序列号"
    w.height = 8
    board_serial = w.inputbox("请输入主板序列号:", default=board_model[:4])[0]
    w.height = 12
else:
    board_model = "A8240"
    board_serial = "A82402010xxx"

os.environ["BOARD_MODEL"] = board_model

top_dir = os.getcwd()

logs_dir = top_dir + "/logs/" + board_model + "/" + board_serial
result_dir = top_dir + "/results/" + board_model + "/" + board_serial
report_dir = top_dir + "/reports/" + board_model + "/" + board_serial


def show_top_menu():
    w.title = "Select test type"
    test_type = w.menu("请选择测试类型：", ("Function", "Performance", "Stability"))
    return test_type


def show_submenu_function():
    w.title = "Select test cases"
    test_cases = w.radiolist("请选择测试用例：", (\
        "All        所有测试用例", \
        "USB        USB接口测试", \
        "SATA       硬盘接口测试", \
        "PCIe       PCIe接口测试"))
    return test_cases 


def show_submenu_performance():
    w.title = "Select test cases"
    test_cases = w.checklist("请选择测试用例：", ("memory", "IO", "network"))
    return test_cases 


def show_submenu_stability():
    w.title = "Select test cases"
    test_cases = w.checklist("请选择测试用例：", (\
        "memtester        内存稳定性测试", \
        "stress           系统压力测试", \
        "iperf            网络稳定性测试", \
        "reboot           多次重启测试"))
    return test_cases 


def run_testcases():
    while True:
        test_type = show_top_menu()
        if test_type[1] == 0:
            if test_type[0] == "Function":
                test_cases = show_submenu_function()
                if test_cases[1] == 0:
                    if "All" in test_cases[0]:
                        pytest.main(["--alluredir={}".format(result_dir), "cases/function"])
                    elif "USB" in test_cases[0]:
                        pytest.main(["--alluredir={}".format(result_dir), "cases/function/test_007_USB.py"])
                    elif "SATA" in test_cases[0]:
                        pytest.main(["--alluredir={}".format(result_dir), "cases/function/test_008_SATA.py"])
                    elif "PCIe" in test_cases[0]:
                        pytest.main(["--alluredir={}".format(result_dir), "cases/function/test_010_pci.py"])
                    else:
                        print("No test cases were selected!")
                        continue
                    break
    
            elif test_type[0] == "Performance":
                test_cases = show_submenu_performance()
                if test_cases[1] == 0:
                    if test_cases[0]:
                        if "IO" in test_cases[0]:
                            print("IO")
                        if "memory" in test_cases[0]:
                            print("memory")
                        if "network" in test_cases[0]:
                            print("network")
                        break
                    else:
                        print("No test cases were selected!")
                continue
    
            elif test_type[0] == "Stability":
                test_cases = show_submenu_stability()
                if test_cases[1] == 0:
                    if test_cases[0]:
                        if "memtester" in str(test_cases[0]):
                            subprocess.run("python cases/stability/case_memtester.py", shell=True, check=True)
                        if "stress" in str(test_cases[0]):
                            subprocess.run("python cases/stability/case_stress.py", shell=True, check=True)
                        if "iperf" in str(test_cases[0]):
                            ret = w.yesno("Is the iperf server started?", default="no")
                            if not ret:
                                subprocess.run("python cases/stability/case_iperf.py", shell=True, check=True)
                            else:
                                w.msgbox("Please start iperf server first!")
                        if "reboot" in str(test_cases[0]):
                            w.msgbox("The reboot test shoud be run manually! \nPlease see Readme.md in cases/stability/reboot.")
                        break
                    else:
                        print("No test cases were selected!")
                continue
        else:
            break


def generate_report():
    """生成测试报告"""
    subprocess.run("allure generate {} -c -o {}".format(result_dir, report_dir), shell=true, stdout=subprocess.pipe, universal_newlines=true, check=true)
    """打开测试报告"""
    subprocess.run("allure open {}".format(report_dir), shell=true, stdout=subprocess.pipe, universal_newlines=true, check=true)


def post_run():
    """测试完成后的操作"""
    del os.environ["BOARD_MODEL"]


try:
    run_testcases()
finally:
    post_run()

