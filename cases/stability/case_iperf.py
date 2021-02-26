
import iperf3
from loguru import logger


# define path of log file
LOG_FILE_PATH = "./logs"
logger.add(LOG_FILE_PATH)

# set iperf client
client = iperf3.Client()
#client.duration = 3600
client.server_hostname = '192.168.0.71'
client.port = 5201
client.protocol = 'udp'
client.bandwidth = 500000000 # 500Mbit/s
client.blksize = 1280 # 越小丢包越多，但超过1448会有警告

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

