import sys as sy
import time as tm
import os
this_dir = os.path.dirname(__file__)
sy.path.append(os.path.join(this_dir, "config"))
import config.motor_pmx_config as cg  # noqa: E402
sy.path.append(os.path.join(this_dir, "src"))
import src.chwpMonitor as cm  # noqa: E402
sy.path.append(os.path.join(this_dir, "PMX", "src"))
import PMX.src.pmx as px  # noqa: E402

# Establish socket connection to remote slowDAQ publisher
monitor = cm.CHWPMonitor()

# Connect to the motor PMX power supply
if cg.use_tcp:
    pmx = px.PMX(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
else:
    pmx = px.PMX(rtu_port=cg.rtu_port)

# Query the gripper status periodically and
# send the data over the socket connection
send_sleep = 100  # sec
try:
    while True:
        # Collect monitoring information
        out_dict = {}
        # Power status
        out_dict.update({"PWR": ("%d" % (int(pmx.check_output())))})
        # Output voltage
        out_dict.update({"VOL": ("%.05f" % (float(pmx.check_voltage())))})
        # Output current
        out_dict.update({"CUR": ("%.05f" % (float(pmx.check_current())))})
        # Send the data
        success = monitor.send_data(out_dict)
        tm.sleep(send_sleep)
except KeyboardInterrupt:
    print("Keyboard Interrupt in 'motor_pmx_monitor.py'")
finally:
    del monitor
