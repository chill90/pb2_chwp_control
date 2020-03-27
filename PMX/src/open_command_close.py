import sys, os
this_dir = os.path.dirname(__file__)
sys.path.append(
    os.path.join(this_dir, '..', 'config'))
sys.path.append(this_dir)

import pmx as pm
import pmx_config as cg
import command as cm
import fcntl as f

def open_command_close(cmd):
    lockfile = open(os.path.join(this_dir, '..', '.port_busy'))
    f.flock(lockfile, f.LOCK_EX | f.LOCK_NB)
    PMX = pm.PMX(rtu_port=cg.rtu_port)
    CMD = cm.Command(PMX)
    result = CMD.user_input(cmd)
    del(PMX,CMD)
    f.flock(lockfile, f.LOCK_UN)
    return result
