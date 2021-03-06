#!/usr/bin/python3

# Built-in python modules
import sys as sy
import argparse as ap
import os

# CHWP control modules
sy.path.append("src")
import src.chwp_control as cc  # noqa: E402

CC = cc.CHWP_Control()
# Allowed command line arguments
cmds = {'warm_grip': CC.warm_grip,
        'cooldown_grip': CC.cooldown_grip,
        'cold_grip': CC.cold_grip,
        'cold_ungrip': CC.cold_ungrip,
        'gripper_home': CC.gripper_home,
        'stop_chwp': CC.stop_chwp,
        'spinup_chwp': CC.spinup_chwp,
        'freq_chwp': CC.freq_chwp,
        'bb_packet_collect': CC.bb_packet_collect}
        # 'gripper_home': CC.gripper_home,
        # 'gripper_reboot': CC.gripper_reboot}

ps = ap.ArgumentParser(
    description="Control program for the PB2bc CHWP")
ps.add_argument('command', choices=cmds.keys())
ps.add_argument('-f', action = 'store', dest = 'freq', type = float, default = 0.0)

args = ps.parse_args()
func = cmds[args.command]

if func == CC.spinup_chwp:
    func(args.freq)
else:
    func()


