import os
import sys
this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, "config"))
sys.path.append(os.path.join(this_dir, "Cyberswitch", "src"))
import cyberswitch_config as cg  # noqa: E402
import NP05B as cs  # noqa: E402

# Connect to the driver board PMX power supplies
if cg.use_tcp:
    pmx_arr = [px.PMX(tcp_ip=ip, tcp_port=port)
               for ip, port in zip(cg.tcp_ips, cg.tcp_ports)]
else:
    pmx_arr = [px.PMX(rtu_port=port) for port in cg.rtu_ports]

# Monitor information
# Power status
pwrs = [pmx.check_output() for pmx in pmx_arr]
pwr_str = ''
for pwr in pwrs:
    pwr_str += ' '.join(pwr)

# Send this information to standard output
wrstr = ("%s") % (pwr_str)
sys.stdout(wrstr)