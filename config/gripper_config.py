# Import global configuration to define the experiment environment
import config.exp_config as cg  # noqa: E402

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
    # Gripper IP port
    tcp_port = 4002
# CHWP Gripper ttyUSB port
else:
    rtu_port = '/dev/ttyUSB1'
