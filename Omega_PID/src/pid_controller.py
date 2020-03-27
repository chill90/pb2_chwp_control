
########################################################################################################################
# Imports
########################################################################################################################

import subprocess, sys, os, fcntl, time
this_dir = os.path.dirname(__file__)
sys.path.append(
    os.path.join(this_dir, '..', 'config'))
import pid_config


########################################################################################################################
# Primary Class
########################################################################################################################

class PID:
    # Information and variables used for PID connection
    def __init__(self, verb = False):
        self.verb = verb
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.return_list = []
        self.PID_INFO = [pid_config.PID_IP, pid_config.PID_PORT]
        self.hex_freq = '00000'
        self.cur_freq = 0
        self.stopping = True
        self.stop_params = [pid_config.stop_p, pid_config.stop_i, pid_config.tune_d]
        self.tune_params = [pid_config.tune_p, pid_config.tune_i, pid_config.tune_d]


########################################################################################################################
# Subprocesses
########################################################################################################################

    # Sets the direction if the CHWP; 0 for forward and 1 for backwards
    def set_direction(self, direction):
        subprocess.call([os.path.join(self.script_dir, 'tune_direction'), self.PID_INFO[0], self.PID_INFO[1],
                         direction], stderr = subprocess.DEVNULL)
        if direction == '0':
            if self.verb:
                print('Forward')
            self.stopping = False
            self.set_pid(self.tune_params)
        elif direction == '1':
            if self.verb:
                print('Reverse')
            self.stopping = True
            self.set_pid(self.stop_params)

    def declare_freq(self, freq):
        if float(freq) <= 3.5:
            self.hex_freq = '0' + self.convert_to_hex(freq, 3)
            if self.verb:
                print('Frequency Setpoint = ' + str(freq) + ' Hz')
        else:
            if self.verb:
                print('Invalid Frequency')

    def convert_to_hex(self, value, decimal):
        temp_value = hex(int(10**decimal*float(value)))
        return ('0000' + str(temp_value)[2:].upper())[-4:]

    def open_line(self):
        while True:
            try:
                self.lock_file = open(os.path.join(this_dir, '.pid_port_busy'))
                fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                time.sleep(2)

    def close_line(self):
        fcntl.flock(self.lock_file, fcntl.LOCK_UN)
        self.lock_file.close()

########################################################################################################################
# Main Processes
########################################################################################################################

    def tune_stop(self):
        self.open_line()
        self.set_direction('1')
        if self.verb:
            print('Starting Stop')
        subprocess.call([os.path.join(self.script_dir, 'tune_stop'), self.PID_INFO[0], self.PID_INFO[1]], 
                         stderr = subprocess.DEVNULL)
        self.close_line()
        self.return_messages()

    def tune_freq(self):
        self.open_line()
        if self.stopping:
            self.set_direction('0')
        if self.verb:
            print('Staring Tune')
        subprocess.call([os.path.join(self.script_dir, 'tune_freq'), self.PID_INFO[0], self.PID_INFO[1],
                         self.hex_freq], stderr = subprocess.DEVNULL)
        self.close_line()
        self.return_messages()

    def get_freq(self):
        self.open_line()
        if self.verb:
            print('Finding CHWP Frequency')
        subprocess.call([os.path.join(self.script_dir, './get_freq'), self.PID_INFO[0], self.PID_INFO[1]],
                         stderr = subprocess.DEVNULL)
        self.open_line()
        self.return_messages()
        return self.cur_freq

    def set_pid(self, params):
        if self.verb:
            print('Setting PID Params')
        p_value = self.convert_to_hex(params[0], 3)
        i_value = self.convert_to_hex(params[1], 0)
        d_value = self.convert_to_hex(params[2], 1)
        subprocess.call([os.path.join(self.script_dir, './set_pid'), self.PID_INFO[0], self.PID_INFO[1], p_value,
                        i_value, d_value], stderr = subprocess.DEVNULL)
        self.return_messages()


########################################################################################################################
# Messaging
########################################################################################################################

    def return_messages(self):
        temp_return = self.read_log()
        self.return_list = self.decode_array(temp_return)
        self.remove_log()

    def read_log(self):
        with open('output.txt', 'rb') as log_file:
            return_string = log_file.read().split(b'\n')[-1]
            return return_string.decode('ascii').split('\r')[:-1]

    def remove_log(self):
        subprocess.call(['rm', 'output.txt'])

    def decode_array(self, input_array):
        output_array = list(input_array)
        
        for index, string in enumerate(list(input_array)):
            header = string[0]
            
            if header == 'R':
                output_array[index] = self.decode_read(string)
            elif header == 'W':
                output_array[index] = self.decode_write(string)
            elif header == 'E':
                output_array[index] = 'PID Enabled'
            elif header == 'D':
                output_array[index] = 'PID Disabled'
            elif header == 'P':
                pass
            elif header == 'G':
                pass
            elif header == 'X':
                output_array[index] = self.decode_measure(string)
            else:
                pass

        return output_array

    def decode_read(self, string):
        read_type = string[1:3]
        if read_type == '01':
            return 'Setpoint = ' + str(int(string[4:], 16)/1000.)
        else:
            return 'Unrecognized Read'

    def decode_write(self, string):
        write_type = string[1:]
        if write_type == '01':
            return 'Changed Setpoint'
        elif write_type == '0C':
            return 'Changed Action Type'
        else:
            return 'Unrecognized Write'

    def decode_measure(self, string):
        measure_type = string[1:3]
        if measure_type == '01':
            self.cur_freq = float(string[3:])
            return float(string[3:])
        else:
            return 9.999


########################################################################################################################
# __main__ for testing
########################################################################################################################

if __name__ == '__main__':
    test_pid = PID()
    #test_pid.declare_freq(input('Set CHWP frequency: '))
    #test_pid.tune_freq()
    #test_pid.get_freq()
    test_pid.tune_stop()
    print(test_pid.return_list)
