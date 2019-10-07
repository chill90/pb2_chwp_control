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
        'gripper_reboot': CC.gripper_reboot}

ps = ap.ArgumentParser(
    description="Control program for the PB2bc CHWP")
ps.add_argument('command', choices=cmds.keys())

args = ps.parse_args()
func = cmds[args.command]
func()
