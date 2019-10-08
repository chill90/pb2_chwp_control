import os
import sys
this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, "config"))
sys.path.append(os.path.join(this_dir, "PMX", "src"))
import exp_config as cg  # noqa: E402
import pmx as px  # noqa: E402

# Connect to the motor PMX power supply
if cg.use_tcp:
    pmx = px.PMX(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
else:
    pmx = px.PMX(rtu_port=cg.rtu_port)

# Monitor information
# Power status
pwr = pmx.check_output()
# Output voltage
vol = pmx.check_voltage()
# Output current
curr = pmx.check_current()

# Send this information to standard output
wrstr = ("%s %.4f %.4f") % (int(pwr), float(vol), float(curr))
sys.stdout(wrstr)
