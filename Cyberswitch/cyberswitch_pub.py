from time import sleep
import sys
import src.open_command_close as occ

sys.path.append('/home/polarbear/slowdaq')

from slowdaq.pb2 import Publisher

pub = Publisher('Cyberswitch','131.243.51.167',3141)
 
while True:    
    try:
        status = occ.open_command_close('status')
    except BlockingIOError:
        print('Busy port! Trying again...')
        sleep(2)
    
    else:
        if status == True:
            continue
        elif len(status) == 5:
            pub.serve()
            data = pub.pack({'Port 1 status: ':status[0],
                             'Port 2 status: ':status[1],
                             'Port 3 status: ':status[2],
                             'Port 4 status: ':status[3],
                             'Port 5 Status: ':status[4]})
            pub.queue(data)
            print('Sending data...')
            sleep(10)  
        else:
            print('Bad output, trying again...')
            sleep(2)

