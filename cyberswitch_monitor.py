import sys as sy
import time as tm
import os
this_dir = os.path.dirname(__file__)
sy.path.append(os.path.join(this_dir, "config"))
import config.cyberswitch_config as cg  # noqa: E402
sy.path.append(os.path.join(this_dir, "src"))
import src.chwpMonitor as cm  # noqa: E402
sy.path.append(os.path.join(this_dir, "Cyberswitch", "src"))
import Cyberswitch.src.NP05B as n5  # noqa: E402


# Establish socket connection to remote slowDAQ publisher
monitor = cm.CHWPMonitor()

# Connect to the driver board PMX power supplies
if cg.use_tcp:
    np05b_arr = [n5.NP05B(tcp_ip=ip, tcp_port=port)
                 for ip, port in zip(cg.tcp_ips, cg.tcp_ports)]
else:
    np05b_arr = [n5.NP05B(rtu_port=port) for port in cg.rtu_ports]


# Query the gripper status periodically and
# send the data over the socket connection
send_sleep = 100  # sec
try:
    while True:
        # Get power status
        out_dict= {}
        out_dict.update(
            {"PWR%02d" % (i): ';'.join(np05b.STATUS())
            for i, np05b in enumerate(np05b_arr)})
        # Send the data
        success = monitor.send_data(out_dict)
        tm.sleep(send_sleep)
except KeyboardInterrupt:
    print("Keyboard Interrupt in 'cyberswitch_monitor.py'")
finally:
    del monitor
