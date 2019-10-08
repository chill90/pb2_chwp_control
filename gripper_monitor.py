import os
import sys
this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, "config"))
sys.path.append(os.path.join(this_dir, "Gripper", "src"))
import gripper_config as cg  # noqa: E402
import C000DRD as c0  # noqa: E402
import JXC831 as jx # noqa: E402
import control as ct # noqa: E402
import gripper as gp # noqa: E402

# Connect to the gripper
if cg.use_tcp:
    plc = c0.C000DRD(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
else:
    plc = c0.C000DRD(rtu_port=cg.rtu_port)
jxc = jx.JXC831(plc)
ctl = ct.Control(jxc)
gpr = gp.Gripper(ctl)

# Retrieve gripper status dictionary
status_dict = gpr.STATUS()
wrstr = ''
for key, value in status_dict.items():
    wrstr += ("%s=%d," % (str(key), int(value)))
# Send this information to standard output
sys.stdout(wrstr)
