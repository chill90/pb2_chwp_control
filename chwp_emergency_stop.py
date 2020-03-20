import sys, os
from time import sleep
this_dir = os.path.dirname(__file__)

sys.path.append(
    os.path.join(this_dir, 'src'))

import chwp_control as cc

sys.path.append(
    os.path.join(this_dir, 'APC_UPS', 'src'))
sys.path.append(
    os.path.join(this_dir, 'APC_UPS', 'config'))

import ups_config
import ups_controller

CC = cc.CHWP_control
ups = ups_controller.UPS(ups_config.ups_ip)

threshold = 50
def main():
    while True:       
        ups.connect()
        ups.update()
        ups.disconnect()

        if ups.battery_percent < threshold:
            break

        sleep(20)

    print('Power failure detected: Stopping CHWP')
    CC.stop_chwp()
    sleep(120)
    print('Regripping')
    CC.cold_grip()
    print('Complete')

if __name__ == '__main__':
    main()
