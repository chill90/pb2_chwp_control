import os
import sys
this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, "config"))
sys.path.append(os.path.join(this_dir, "Cyberswitch", "src"))
import cyberswitch_config as cg  # noqa: E402
import NP05B as n5  # noqa: E402

# Connect to the driver board PMX power supplies
if cg.use_tcp:
    np05b_arr = [n5.NP05B(tcp_ip=ip, tcp_port=port)
                 for ip, port in zip(cg.tcp_ips, cg.tcp_ports)]
else:
    np05b_arr = [n5.NP05B(rtu_port=port) for port in cg.rtu_ports]

# Monitor information
# Power status
outs = [np05b.check_output() for np05b in np05b_arr]
out_str = ''
for out in outs:
    out_str += ' '.join(out)

# Send this information to standard output
wrstr = ("%s") % (out_str)
sys.stdout(wrstr)
