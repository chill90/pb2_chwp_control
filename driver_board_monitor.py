import os
import sys
this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, "config"))
sys.path.append(os.path.join(this_dir, "PMX", "src"))
import driver_board_pmx_config as cg  # noqa: E402
import pmx as px  # noqa: E402

# Connect to the driver board PMX power supplies
if cg.use_tcp:
    pmx_arr = [px.PMX(tcp_ip=ip, tcp_port=port)
               for ip, port in zip(cg.tcp_ips, cg.tcp_ports)]
else:
    pmx_arr = [px.PMX(rtu_port=port) for port in cg.rtu_ports]

# Monitor information
# Power status
pwrs = [int(pmx.check_output()) for pmx in pmx_arr]
# Output voltage
vols = [float(pmx.check_voltage()) for pmx in pmx_arr]
# Output current
currs = [float(pmx.check_current()) for pmx in pmx_arr]

# Send this information to standard output
wrstr = ("%s %s %.4f %.4f %.4f %.4f") % (*pwrs, *vols, *currs)
sys.stdout(wrstr)