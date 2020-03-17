#!/usr/bin/python3

# Built-in python functions
import sys as sys
from time import sleep
import src.open_command_close as occ

# Check the python version
if sys.version_info.major == 2:
    print(
        "\nKikusui PMX control only works with Python 3\n"
        "Usage: sudo python3 command_supply.py")
    sys.exit()

# Connect to PMX power supply
#if cg.use_moxa:
#    PMX = pm.PMX(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
#else:

# Check if inputs were passed via the command line
if len(sys.argv) > 1:
    command = ' '.join(sys.argv[1:])
    while True:
        try:
            occ.open_command_close(command)
        except BlockingIOError:
            print('Busy port, try again!')

else:
    while True:
        command = input("Enter command ('H' for help): ")
        if command.strip() == '':
            continue
        try:
            occ.open_command_close(command)
        except BlockingIOError:
            print('Busy port, try again!')
            
