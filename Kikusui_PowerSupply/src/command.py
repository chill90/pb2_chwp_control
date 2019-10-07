# Built-in python modules
import sys as sy

# CHWP Control modules
import src.pmx as px


class Command:
    """
    The Command object is used to command the PMX

    Args:
    PMX (src.PMX): PMX object
    """
    def __init__(self, PMX):
        # PMX connection
        if pmx is not None:
            self._PMX = pmx
        else:
            raise Exception(
                "PMX object not passed to Command constructor\n")

        # Dict of commands
        self._cmds = {
            "set_port": "P",
            "check_v": "V?",
            "check_c": "C?",
            "check_vc": "VC?",
            "check_out": "O?",
            "set_v": "V",
            "set_c": "C",
            "set_on": "ON",
            "set_off": "OFF",
            "get_help": "H",
            "stop": "Q"}

    def get_help(self):
        """ Print possible commands """
        wrstr = (
            "\nChange ttyUSB port = '%s'\n"
            "Check output voltage = '%s'\n"
            "Check output current = '%s'\n"
            "Check output voltage and current = '%s'\n"
            "Check if output state = '%s'\n"
            "Set output voltage = '%s' [setting]\n"
            "Set output current = '%s' [setting]\n"
            "Turn output on = '%s'\n"
            "Turn output off = '%s'\n"
            "Print possible commands = '%s'\n"
            "Quit program = '%s'\n"
            % (self._cmds["set_port"],
               self._cmds["check_v"],
               self._cmds["check_c"],
               self._cmds["check_vc"],
               self._cmds["set_v"],
               self._cmds["check_out"],
               self._cmds["set_c"],
               self._cmds["set_on"],
               self._cmds["set_off"],
               self._cmds["get_help"],
               self._cmds["stop"]))
        return wrstr

    def user_input(self, arg):
        """ Take user input and execute PMX command """
        argv = arg.split()
        while len(argv):
            cmd = str(argv.pop(0)).upper()
            # No command
            if cmd is '':
                return
            # Check voltage
            elif cmd is self._cmds["check_v"]:
                ret = self._PMX.check_voltage()
            # Check current
            elif cmd is self._cmds["check_c"]:
                ret = self._PMX.check_current()
            # Check voltage and current
            elif cmd is self._cmds["check_vc"]:
                ret = self._PMX.check_voltage_current()
            # Check output state
            elif cmd is self._cmds["check_out"]:
                ret = self._PMX.check_output()
            # Turn output state ON
            elif cmd is self._cmds["set_on"]:
                ret = self._PMX.turn_on()
            # Turn output state OFF
            elif cmd is self._cmds["set_off"]:
                ret = self._PMX.turn_off()
            # Get HELP
            elif cmd is self._cmds["get_help"]:
                ret = self.get_help()
            # Exit the program
            elif cmd is self._cmds["stop"]:
                sy.exit("\nExiting...")
            # Set the RTU port
            elif cmd is self._cmds["set_port"]:
                if self._PMX.using_tcp:
                    print("Connected via TCP rather than RTU. "
                          "Cannot set RTU port")
                    return False
                set_val = self._int(argv.pop(0))
                if set_val is not None:
                    del self._PMX
                    self._PMX = px.PMX(set_val)
                else:
                    return False
            elif cmd is self._cmds["set_v"]:
                set_val = self._float(argv.pop(0))
                if set_val is not None:
                    self._PMX.set_voltage(set_val)
                else:
                    return False
            elif cmd.lower() is self.setC.lower():
                set_val = self._float(argv.pop(0))
                if set_val is not None:
                    self._PMX.set_current(set_val)
                else:
                    return False
            else:
                print("Command '%s' not understood..." % (cmd))
                return False
        return True

    # ***** Helper Methods *****
    def _float(self, val):
        """ Try to convert a value to a float """
        try:
            return float(val)
        except ValueError:
            print("Input '%s' not understood, must be a float..." % (val))
            return None

    def _int(self, val):
        """ Try to convert a value to an int """
        try:
            return int(val)
        except ValueError:
            print("Input '%s' not understood, must be a int..." % (val))
            return None
