# Import global configuration to define the experiment environment
import sys as sy
import os

this_dir = os.path.dirname(__file__)
sy.path.append(os.path.join(
    this_dir, '..', '..', '..', 'config'))
import exp_config as cg

exp = cg.exp
# Boolean flag for Ethernet to IP
if exp == 'PB2b':
    use_tcp = True
elif exp == 'SO':
    use_tcp = False
else:
    use_tcp = False

# MOXA IP address
if use_tcp:
    tcp_ip = '192.168.2.52'
    tcp_port = 4002
# CHWP Gripper ttyUSB port
else:
    rtu_port = '/dev/ttyUSB1'
