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
    tcp_ips = ['192.168.2.56', '192.168.2.56']
    tcp_ports = [4003, 4004]
# CHWP Gripper ttyUSB port
else:
    rtu_ports = ['/dev/ttyUSB1', '/dev/ttyUSB2']