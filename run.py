# entry
import subprocess
from loguru import logger
from whiptail import Whiptail

w = Whiptail(width=50, height=12)

def show_top_menu():
    w.title = "Select test type"
    test_type = w.menu("请选择测试类型：", ["Function", "Performance", "Stability"])
    return test_type

def show_submenu_function():
    w.title = "Select test cases"
    test_cases = w.checklist("请选择测试用例：", ["CPU", "memory", "storage", "network"])
    return test_cases 

def show_submenu_performance():
    w.title = "Select test cases"
    test_cases = w.checklist("请选择测试用例：", ["memory", "IO", "network"])
    return test_cases 

def show_submenu_stability():
    w.title = "Select test cases"
    test_cases = w.checklist("请选择测试用例：", ["memtester", "stress", "iperf", "reboot"])
    return test_cases 

while True:
    test_type = show_top_menu()
    if test_type[1] == 0:
        if test_type[0] == "Function":
            test_cases = show_submenu_function()
            if test_cases[1] == 0:
                if test_cases[0]:
                    if "CPU" in test_cases[0]:
                        print("CPU")
                    if "memory" in test_cases[0]:
                        print("memory")
                    if "storage" in test_cases[0]:
                        print("storage")
                    if "network" in test_cases[0]:
                        print("network")
                    break
                else:
                     print("No test cases were selected!")
            continue

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
                    if "memtester" in test_cases[0]:
                        subprocess.run("python cases/stability/case_memtester.py", shell=True, check=True)
                    if "stress" in test_cases[0]:
                        subprocess.run("python cases/stability/case_stress.py", shell=True, check=True)
                    if "iperf" in test_cases[0]:
                        ret = w.yesno("Is the iperf server started?", default="no")
                        if not ret:
                            subprocess.run("python cases/stability/case_iperf.py", shell=True, check=True)
                        else:
                            w.msgbox("Please start iperf server first!")
                    if "reboot" in test_cases[0]:
                        w.msgbox("The reboot test shoud be run manually! \nPlease see Readme.md in cases/stability/reboot.")
                    break
                else:
                    print("No test cases were selected!")
            continue

    else:
        break
