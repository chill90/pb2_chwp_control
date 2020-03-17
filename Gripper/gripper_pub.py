from time import sleep
import sys
import src.open_command_close as occ

sys.path.append('/home/polarbear/slowdaq')

from slowdaq.pb2 import Publisher

pub = Publisher('Gripper','131.243.51.167',3141)

while True:
    try:
        status = occ.open_command_close('status')        
    except BlockingIOError:
        print('Busy! Trying again...')
        sleep(2)
    else:
        if type(status) == dict:
            pub.serve()
            data = pub.pack(status)
            pub.queue(data)
            print('Sending data...')
            sleep(10)
        else:
            print('Bad output, trying again...')
            sleep(2)
