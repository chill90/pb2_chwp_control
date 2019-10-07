from __future__ import print_function

import sys           as sy
import readline

import src.NP_05B           as np
import src.command_NP_05B   as cm

        
if __name__ == "__main__":
    if cg.use_moxa:
        NP05B = np.NP_05B(tcp_ip=cg.moxa_ip, tcp_port=cg.moxa_port)
    else:
        NP05B = np.NP_05B(rtu_port=cg.ttyUSBPort)
    CMD = cm.Command(NP05B)

    #If user supplies a command-line argument, interpret it as a command to the cyberswitch
    if len(sy.argv[1:]) > 0:
        args = sy.argv[1:]
        command = ' '.join(args)
        result = CMD.CMD(command)
    else:
        #Otherwise, ask the user for a command
        while True:
            command = raw_input('Cyberswitch command [HELP for help]: ')
            result = CMD.CMD(command)
            if result is True:
                print('Notification in cyberswtich_command(): Command executed successfully')
            elif result is False:
                print('Error in cyberswitch_command(): Command failed...')
            else:
                pass
