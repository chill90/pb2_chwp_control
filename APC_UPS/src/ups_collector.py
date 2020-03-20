import os, sys
from time import sleep

this_dir = os.path.dirname(__file__)
sys.path.append(
    os.path.join(this_dir, '..', 'config'))
sys.path.append(this_dir)

import ups_config
import ups_controller

# Change this to the directory which holds slowdaq
slowdaq_dir = ''
sys.path.append(slowdaq_dir)
from slowdaq3.slowdaq.pb2 import Publisher

pub = Publisher('ups_info', ups_config.aggregator_ip, ups_config.aggregator_port)
ups = ups_controller.UPS(ups_config.ups_ip)

i = 0
def main():
    while True:
        pub.serve()

        ups.connect()
        ups.update()
        ups.disconnect()
        data = pub.pack({'output_info': ups.output_info, 'input_info': ups.input_info,
                         'battery_percent': ups.battery_percent, 'battery_temp': ups.battery_temperature,
                         'battery_life': ups.battery_life})
        pub.queue(data)

        i += 1
        if not i % 2:
            while len(pub.inbox) > 0:
                print pub.inbox.pop()

        sleep(10)

if __name__ == '__main__':
    main()
