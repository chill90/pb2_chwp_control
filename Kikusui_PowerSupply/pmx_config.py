# Boolean flag for Ethernet to IP
use_tcp = False

# MOXA IP address
tcp_ip = '192.168.2.52'
tcp_port = 4002

# CHWP Gripper ttyUSB port
if not use_tcp:
    rtu_port = '/dev/ttyUSB1'
