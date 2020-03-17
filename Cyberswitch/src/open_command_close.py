import src.NP05B as np
import config.config_NP05B as cg
import src.command_NP05B as cm
import fcntl as f

def open_command_close(cmd):
    lockfile = open('.port_busy')
    f.flock(lockfile, f.LOCK_EX | f.LOCK_NB)
    NP05B = np.NP05B(rtu_port=cg.rtu_port)
    CMD = cm.Command(NP05B)
    result = CMD.CMD(cmd)
    del(NP05B,CMD)
    f.flock(lockfile, f.LOCK_UN)
    return result
