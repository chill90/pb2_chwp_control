# slowdaw publisher for Omega PID controller

# Imports
import os, sys
from time import sleep

this_dir = os.path.dirname(__file__)
sys.path.append(
    os.path.join(this_dir, '..', 'config'))
sys.path.append(this_dir)

import pid_config
import pid_controller

# Change this to the directory which holds slowdaq
slowdaq_dir = ''
sys.path.append(slowdaq_dir)
from slowdaq3.slowdaq.pb2 import Publisher

# Instantiates a publisher instance for the PID controller
pub = Publisher('pid_info', pid_config.aggregator_ip, pid_config.aggregator_port)
pid = pid_controller.PID()

# Every 10 seconds send the CHWP frequency to slowdaq
i = 0
def main():
    while True:
        pub.serve()

        pid.get_freq()
        data = pub.pack({'chwp_freq': pid.cur_freq})
        pub.queue(data)

        i += 1
        if not i % 2:
            while len(pub.inbox) > 0:
                print(pub.inbox.pop())

        sleep(10)

if __name__ == '__main__':
    main()
