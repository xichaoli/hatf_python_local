"""
Copyright(C), ZYTC
File name: case_iperf.py
Author: lixc
Version: 0.1
Date: 2021-03-05
Description: Measure packet loss and jitter.
"""
import os
import time
import iperf3
from loguru import logger
from whiptail import Whiptail


# define path of log file
time_now = time.strftime("%Y%m%d_%H:%M:%S", time.localtime())
logs_top_dir = os.getenv("LOGS_DIR")
LOG_FILE_PATH = logs_top_dir + "/network_test_" + time_now
logger.add(LOG_FILE_PATH)

# set iperf client
client = iperf3.Client()

w = Whiptail(width=50, height=8)
client.protocol = 'udp'
client.blksize = 1280 # 越小丢包越多，但超过1448会有警告
client.server_hostname = w.inputbox("请输入 iperf 服务器地址：", default="192.168.0.89")[0]
client.port = int(w.inputbox("请输入 iperf 服务器端口号：", default="5201")[0])
client.bandwidth = int(w.inputbox("请输入目标测试带宽(bits/s)", default="500000000")[0])
client.duration = int(w.inputbox("请输入测试持续时间：(s)", default="3600")[0])

logger.info('\nStart iperf test. Connecting to {0}:{1}'.format(client.server_hostname, client.port))
result = client.run()

if result.error:
    logger.error(result.error)
else:
    logger.info('')
    logger.info('Iperf test completed:')
    logger.info('  started at                     {0}'.format(result.time))
    logger.info('  duration (s)                   {0}'.format(result.duration))
    logger.info('  transmitted                    {0}'.format(result.bytes))
    logger.info('  lost packets                   {0}'.format(result.lost_packets))
    logger.info('  lost percent                   {0}'.format(result.lost_percent))
    logger.info('  jitter (ms)                    {0}'.format(result.jitter_ms))
    logger.info('  Megabits per second  (Mbps)    {0}'.format(result.Mbps))

