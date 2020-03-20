import telnetlib, sys, fcntl, sleep

class UPS:
    def __init__(self, ups_ip, lock_file_name = '.apc1_port_busy'):
        self.HOST = ups_ip
        self.USER = 'apc'
        self.PASSWORD = 'apc'
        self.lock_file_name = lock_file_name

        self.connect()
        self.update()
        self.disconnect()

    def connect(self):
        while True:
            try:
                self.lock_file = open(self.lock_file_name)
                fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                time.sleep(2)
        
        try:
            self.network = telnetlib.Telnet(self.HOST)

            self.network.read_some()
            self.network.write(self.USER.encode('ascii') + b'\r')
            self.network.read_some()
            self.network.write(self.PASSWORD.encode('ascii') + b'\r')
        except:
            print('ERROR: Cannot connect to UPS')
            sys.exit()

    def disconnect(self):
        self.network.write(b'exit\r')
        fcntl.flock(self.lock_file, fcntl.LOCK_UN)
        self.lock_file.close()

    def update(self):
        self.input_cable()
        self.battery_charge()
        self.battery_temp()
        self.runtime()
        self.output_cable()

    def input_cable(self):
        self.network.write(b'detstatus -im\r')
        
        self.network.read_until(b'Input ')
        info = self.network.read_until(b' Hz').decode('ascii')
        info = info.replace('Input ','')
        self.input_info = info.split('\r\n')

    def battery_charge(self):
        self.network.write(b'detstatus -soc\r')

        self.network.read_until(b'Battery State Of Charge: ')
        self.battery_percent = self.network.read_until(b' %').decode('ascii')

    def battery_temp(self):
        self.network.write(b'detstatus -tmp\r')

        self.network.read_until(b'Battery Temperature: ')
        self.battery_temperature = self.network.read_until(b' C').decode('ascii')

    def runtime(self):
        self.network.write(b'detstatus -rt\r')

        self.network.read_until(b'Runtime Remaining: ')
        self.battery_life = self.network.read_until(b' sec').decode('ascii')

    def output_cable(self):
        self.network.write(b'detstatus -om\r')

        self.network.read_until(b'Output ')
        info = self.network.read_until(b' kWh').decode('ascii')
        info = info.replace('Output ','')
        self.output_info = info.split('\r\n')

if __name__ == '__main__':
    MUX2_UPS = UPS('192.168.2.60')
    print("Output Info:", MUX2_UPS.output_info)
    print("Input Info:", MUX2_UPS.input_info)
    print("Battery Percentage", MUX2_UPS.battery_percent)
    print("Battery Temperature", MUX2_UPS.battery_temperature)
    print("Battery Time Left", MUX2_UPS.battery_life)
