import src.pmx as pm
import config.pmx_config as cg
import src.command as cm
import fcntl as f

def open_command_close(cmd):
    lockfile = open('.port_busy')
    f.flock(lockfile, f.LOCK_EX | f.LOCK_NB)
    PMX = pm.PMX(rtu_port=cg.rtu_port)
    CMD = cm.Command(PMX)
    result = CMD.user_input(cmd)
    del(PMX,CMD)
    f.flock(lockfile, f.LOCK_UN)
    return result
