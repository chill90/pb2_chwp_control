#!/usr/bin/python3

# Built-in python functions
import sys as sy
import readline

# Check the python version
if sy.version_info.major == 2:
    print(
        "\nKikusui PMX control only works with Python 3\n"
        "Usage: sudo python3 command_supply.py")
    sy.exit()

# Import CHWP control modules
sy.path.append('src')
import pmx_config as cg  # noqa: E402
import src.pmx as pm  # noqa: E402
import src.command as cm  # noqa: E402

# Connect to PMX power supply
if cg.use_moxa:
    PMX = pm.PMX(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
else:
    PMX = pm.PMX(rtu_port=cg.rtu_port)
cmd = cm.Command(PMX)

# Check if inputs were passed via the command line
if len(sy.argv) > 1:
    val = ' '.join(sy.argv[1:])
    cmd.user_input(val)
else:
    while True:
        val = input("Enter command ('H' for help): ")
        cmd.user_input(val)
