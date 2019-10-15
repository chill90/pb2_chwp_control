import socket as sk
import sys as sy
import os
this_dir = os.path.dirname(__file__)
sy.path.append(os.path.join(this_dir, "..", "config"))
import config.socket_config as sg  # noqa: E402


class CHWPMonitor(object):
    def __init__(self):
        # Establish socket connection to remote slowDAQ publisher
        self.s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.s.bind((sg.remote_ip, sg.remote_port))
        self.s.listen(sg.conn_attempts)
        self._recv_size = 1024
    
    def __del__(self):
        self.close_socket()

    def send_data(self, data_dict):
        # Check to see if data was requested
        req_string = self.s.recv(self._recv_size).strip().upper()
        if req_string == "REQDATA":
            self._package_data(data_dict)
            self.s.send(self._data_to_send)
            return True
        elif req_string == "":
            return False
        else:
            print("Unexpected string received in CHWPMonitor: %s"
                  % (req_string))
            return False

    def close_socket(self):
        self.s.shutdown(sk.SHUT_RDWR)
        self.s.close()
        return

    def _package_data(self, data_dict):
        # Construct a string to be sent to the slowDAQ publisher
        # with the following format
        # "key1,key2,...,keyn:val1,val2,...,valn"
        wrstr = ''
        for key in data_dict.keys():
            if key != data_dict.keys()[-1]:
                wrstr += ("%s," % (str(key)))
            else:
                wrstr += ("%s:" % (str(key)))
        for val in data_dict.values():
            if val != data_dict.values()[-1]:
                wrstr += ("%01d," % (int(val)))
            else:
                wrstr += ("%01d" % (int(val)))
        self._data_to_send = wrstr
        return
    