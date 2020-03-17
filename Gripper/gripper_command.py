#!/usr/bin/python3

# Built-in python modules
import sys 
from time import sleep
import src.open_command_close as occ

# Check python version -- only python3 allowed
if sys.version_info.major == 2:
    print("\nOnly Python 3 supported.")
    print("Usage: sudo python3 gripper_command.py [cmd]")
    sys.exit()

###
#if cg.use_tcp:
#    PLC = c0.C000DRD(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
#else:
    #PLC = c0.C000DRD(rtu_port=cg.rtu_port)
#JXC = jx.JXC831(PLC)
#CTL = ct.Control(JXC)
#GPR = gp.Gripper(CTL)
#CMD = cd.Command(GPR)
###

# Execute user argument
# Command passed from the command line?
if len(sys.argv) > 1:
    command = ' '.join(sys.argv[1:])
    while True:
        try:
            occ.open_command_close(command)
        except BlockingIOError:
            print('Busy port, try again!')

# Prompt user for command at command line
else:
    while True:
        command = input("Gripper command ('HELP' for help): ")
        if command.strip() == '':
            continue
        try: 
            occ.open_command_close(command)
        except BlockingIOError:
            print('Busy port, try again!')
            
      
