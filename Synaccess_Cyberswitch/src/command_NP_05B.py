class Command:
    def __init__(selfm, NP05B):
        if NP05B is None:
            raise Exception(
                "Must provide NP05B object to Command_NP_05B() init function")
        else:
            self._NP05B = NP05B
            self._log = self._NP05B.log
        return

    def HELP(self):
        wrstr = (
            "\nAvailable commands to the NP-05B Cyberswitch:\n"
            "ON [port]:  turn on port [port], for which the options are 1-5\n"
            "OFF [port]: turn off port [port], for which the options are 1-5\n"
            "ALL ON:  turn on all ports\n"
            "ALL OFF: turn off all ports\n"
            "REBOOT [port]: reboot port [port], for which the options are 1-5"
            "STATUS: print status of each port"
            "HELP: display this help menu"
            "EXIT: quit program\n")
        print(wrstr)
        return True

    def CMD(self, cmd):
        args = cmd.split()
        if len(args) == 0:
            return None
        cmdarg = args[0].upper()
        # Turn on/off or reboot specific port
        if cmdarg == 'ON' or cmdarg == 'OFF' or cmdarg == 'REBOOT':
            if len(args) == 2 and args[1].isdigit():
                port = int(args[1])
                if port <= 5 and port >= 1:
                    if cmdarg == 'ON':
                        self._NP05B.ON(port)
                    elif cmdarg == 'OFF':
                        self._NP05B.OFF(port)
                    elif cmdarg == 'REBOOT':
                        self._NP05B.REBOOT(port)
                    else:
                        self._log.err(
                            "Parsing error for command %s" % (' '.join(args)))
                        return False
                else:
                    self._log.err(
                        "Provided port %d not in allowed range 1-5")
                    return False
            else:
                self._log.err(
                    "Could not understand command %s" % (cmd))
                return False
        # Turn on/off or reboot all ports
        elif cmdarg == 'ALL':
            if args[1].upper() == 'ON':
                self._NP05B.ALL_ON()
            elif args[1].upper() == 'OFF':
                self._NP05B.ALL_OFF()
            else:
                self._log.err("Could not understand command %s" % (cmd))
                return False
        # Retrieve port status
        elif cmdarg == 'STATUS':
            outputs = self._NP05B.STATUS()
            self._log.out("\nPort power status:")
            for i in range(len(outputs)):
                self._log.out(
                    "Port %d = %s\n"
                    % (i + 1, bool(int(outputs[i]))))
        # Print help menu
        elif cmdarg == 'HELP':
            HELP()
        # Exit the program
        elif cmdarg == 'EXIT':
            self._log.out("Exiting...")
            sy.exit(0)
        else:
            self._log.err("Could not understand command %s" % (cmd))
            return False
        return True
