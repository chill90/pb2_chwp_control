from time import sleep
import sys
import src.open_command_close as occ

sys.path.append('/home/polarbear/slowdaq')

from slowdaq.pb2 import Publisher

pub = Publisher('PMX1','131.243.51.167',3141)

while True:
    try:
        voltage, current = occ.open_command_close('VC?')
        output = occ.open_command_close('O?')[1]
    except BlockingIOError:
        print('Busy port! Trying again...')
        sleep(2)
    else:
        if type(voltage)==float and type(current)==float and type(output)==int:
            pub.serve()
            data = pub.pack({'Measured voltage':voltage,
                             'Measured current':current,
                             'Output status':output})
            print('Sending data')
            pub.queue(data)
            sleep(10)
        else:
            print('Bad outputs! trying again...')
            sleep(2)

