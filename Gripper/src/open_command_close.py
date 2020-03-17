import config.gripper_config as cg
import src.C000DRD as c0
import src.JXC831 as jx
import src.control as ct
import src.gripper as gp
import src.command_gripper as cd
import fcntl as f

def open_command_close(cmd):
    lockfile = open('.port_busy')
    f.flock(lockfile, f.LOCK_EX | f.LOCK_NB)
    PLC = c0.C000DRD(rtu_port=cg.rtu_port)
#    print('Port opened')
    JXC = jx.JXC831(PLC)
    CTL = ct.Control(JXC)
    GPR = gp.Gripper(CTL)
    CMD = cd.Command(GPR)
    result = CMD.CMD(cmd)
#    print('Command sent')
#    print('Port closed')
    del(PLC,JXC,CTL,GPR,CMD)
    f.flock(lockfile, f.LOCK_UN)
    return result
