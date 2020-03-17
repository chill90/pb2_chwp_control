import sys
from time import sleep
import src.open_command_close as occ

if __name__ == "__main__":
#    if cg.use_moxa:
#        NP05B = np.NP_05B(tcp_ip=cg.moxa_ip, tcp_port=cg.moxa_port)
#    else:

    #If user supplies a command-line argument, interpret it as a command to the cyberswitch
    if len(sys.argv[1:]) > 0:
        command = ' '.join(sys.argv[1:])
        while True:
            try:
                occ.open_command_close(command)
            except BlockingIOError:
                print('Busy port, try again!')
    else:
        #Otherwise, ask the user for a command
        while True:
            command = input('Cyberswitch command [HELP for help]: ')
            if command.strip() == '':
                continue
            try:
                occ.open_command_close(command) 
            except BlockingIOError:
                print('Busy port, try again!')
                
                

