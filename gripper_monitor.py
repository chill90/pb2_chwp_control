import sys as sy
import time as tm
import os
this_dir = os.path.dirname(__file__)
sy.path.append(os.path.join(this_dir, "config"))
import config.gripper_config as cg  # noqa: E402
sy.path.append(os.path.join(this_dir, "src"))
import src.chwpMonitor as cm  # noqa: E402
sy.path.append(os.path.join(this_dir, "Gripper", "src"))
import Gripper.src.C000DRD as c0  # noqa: E402
import Gripper.src.JXC831 as jx  # noqa: E402
import Gripper.src.control as ct  # noqa: E402
import Gripper.src.gripper as gp  # noqa: E402


# Establish socket connection to remote slowDAQ publisher
monitor = cm.CHWPMonitor()

# Connect to the gripper
if cg.use_tcp:
    plc = c0.C000DRD(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
else:
    plc = c0.C000DRD(rtu_port=cg.rtu_port)
jxc = jx.JXC831(plc)
ctl = ct.Control(jxc)
gpr = gp.Gripper(ctl)

# Query the gripper status periodically and send the data over
# the socket connection
send_sleep = 100  # sec
try:
    while True:
        # Retrieve gripper status dictionary
        out_dict = gpr.STATUS()

        # Send the data
        monitor.send_data(out_dict)
        tm.sleep(send_sleep)
except KeyboardInterrupt:
    print("Keyboard Interrupt in 'gripper_monitor.py'")
finally:
    del monitor
