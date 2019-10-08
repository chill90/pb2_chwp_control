#!/usr/bin/python3

# Built-in python modules
import sys as sy
import readline

# Check python version -- only python3 allowed
if sy.version_info.major == 2:
    print("\nOnly Python 3 supported.")
    print("Usage: sudo python3 gripper_command.py [cmd]")
    sy.exit()

# Gripper modules
sy.path.append('src')
sy.path.append('config')
import config.gripper_config as cg  # noqa: E402
import src.C000DRD as c0  # noqa: E402
import src.JXC831 as jx  # noqa: E402
import src.control as ct  # noqa: E402
import src.gripper as gp  # noqa: E402
import src.command_gripper as cd  # noqa: E402

if cg.use_tcp:
    PLC = c0.C000DRD(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
else:
    PLC = c0.C000DRD(rtu_port=cg.rtu_port)
JXC = jx.JXC831(PLC)
CTL = ct.Control(JXC)
GPR = gp.Gripper(CTL)
CMD = cd.Command(GPR)

# Execute user argument
# Command passed from the command line?
if len(sy.argv) > 1:
    user_input = ' '.join(sy.argv[1:])
    CMD.CMD(GPR, user_input)
# Prompt user for command at command line
else:
    while True:
        try:
            user_input = input("Gripper command ('HELP' for help): ")
            if user_input.strip() == '':
                continue
            CMD.CMD(user_input)
        except KeyboardInterrupt:
            GPR.OFF()
            sy.exit('\nExiting gripper_control\n')
