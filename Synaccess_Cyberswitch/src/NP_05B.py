# Built-in python modules
import time as tm
import serial as sr
import sys as sy
import os

# CHWP control modules
this_dir = os.path.dirname(__file__)
sy.path.append(this_dir)
sy.path.append(
    os.path.join(this_dir, "..", "config"))
moxa_path = os.path.join(this_dir, "..", "..", "..", "MOXA")
if moxa_path not in sy.path:
    sy.path.append(moxa_path)
import config_NP_05B as cg  # noqa: E402
import log_NP_05B as lg  # noqa: E402
import moxaSerial as mx  # noqa: E402


class NP_05B:
    """
    The NP_05B object for communicating with the Synaccess Cyberswitch

    Args:
    Args:
    rtu_port (int): Modbus serial port (defualt None).
    tcp_ip (str): TCP IP address (default None)
    tcp_port (int): TCP IP port (default None)

    Only either rtu_port or tcp_ip + tcp_port can be defined.
    """
    def __init__(self, rtu_port=None, tcp_ip=None, tcp_port=None):
        # Logging object
        self.log = lg.Logging()

        # Connect to device
        if rtu_port is None and tcp_ip is None and tcp_port is None:
            if cg.use_tcp:
                self.__conn(tcp_ip=cg.tcp_ip, tcp_port=cg.tcp_port)
            else:
                self.__conn(rtu_port=cg.rtu_port)
        else:
            self.__conn(rtu_port, tcp_ip, tcp_port)

        # Read parameters
        self._num_tries = 10
        self._bytes_to_read = 20
        self._tstep = 0.2

    def __del__(self):
        if not self.use_tcp:
            self.log.log(
                "Closing RTU serial connection at port %s"
                % (self._rtu_port))
            self._clean_serial()
            self._ser.close()
        else:
            self.log.log(
                "Closing TCP connection at IP %s and port %s"
                % (self._tcp_ip, self._tcp_port))
            pass
        return

    def ON(self, port):
        """ Power on a specific port """
        cmd = '$A3 %d 1' % (port)
        self._command(cmd)
        return self.check_output(cmd)

    def OFF(self, port):
        """ Power off a specific port """
        cmd = '$A3 %d 0' % (port)
        self._command(cmd)
        return self._check_output(cmd)

    def ALL_ON(self):
        """ Power on all ports """
        cmd = '$A7 1'
        self._command(cmd)
        return self._check_output(cmd)

    def ALL_OFF(self):
        """ Power off all ports """
        cmd = '$A7 0'
        self._command(cmd)
        return self.check_output(cmd)

    def REBOOT(self, port):
        """ Reboot a specific port """
        cmd = '$A4 %d' % (port)
        self._command(cmd)
        return self._check_output()

    def STATUS(self):
        """ Print the power status for all ports """
        cmd = '$A5'
        for n in range(self._num_tries):
            self._write(cmd)
            out = self._read()
            if len(out) == 0:
                continue
            elif cmd in out:
                return list(out.lstrip(cmd).strip())[::-1]
            else:
                self.log.err(
                    "Did not understand NP_05B output %s" % (out))
                continue
        return False

    # ***** Helper methods *****
    def __conn(self, rtu_port=None, tcp_ip=None, tcp_port=None):
        """ Connect to device either via TCP or RTU """
        if rtu_port is None and (tcp_ip is None or tcp_port is None):
            raise Exception('NP_05B Exception: no RTU or TCP port specified')
        elif (rtu_port is not None and
              (tcp_ip is not None or tcp_port is not None)):
            raise Exception(
                "NP_05B Exception: RTU and TCP port specified. "
                "Can only have one or the other.")
        elif rtu_port is not None:
            self._ser = sr.Serial(
                port=rtu_port, baudrate=9600, bytesize=8,
                parity='N', stopbits=1, timeout=1)
            self.log.log(
                "Connecting to RTU serial port %s" % (rtu_port))
            self.use_tcp = False
            self._rtu_port = rtu_port
        elif tcp_ip is not None and tcp_port is not None:
            self._ser = mx.Serial_TCPServer((tcp_ip, tcp_port))
            self.log.log(
                "Connecting to TCP IP %s via port %d"
                % (tcp_ip, int(tcp_port)))
            self.use_tcp = True
            self._tcp_ip = tcp_ip
            self._tcp_port = tcp_port

    def _wait(self):
        """ Wait a specific timestep """
        time.sleep(self._tstep)
        return True

    def _clean_serial(self):
        """ Flush the serial buffer """
        if not self.use_tcp:
            self._ser.reset_input_buffer()
            self._ser.reset_output_buffer()
            self._ser.flush()
        else:
            self._ser.flushInput()
        return

    def _write(self, cmd):
        """ Write to the serial port """
        self._clean_serial()
        self._ser.write((cmd+'\r'))
        self._wait()

    def _read(self):
        """ Read from the serial port """
        if not self._use_tcp:
            return self._ser.readlines()
        else:
            raw_out = self._ser.read(self.bytes_to_read)
            out = raw_out.replace('\r', ' ').replace('\x00', '')
            return out

    def _check_output(self, cmd):
        """ Check the output """
        out = self._read()
        if len(out) == 0:
            return False
        elif cmd.split()[0] in out.split()[0] and '$A0' in out:
            return True
        elif not len([s for s in out if 'Telnet active.' in s]) == 0:
            self.log.log('Telnet active. Resetting... try command again.')
            return self._deactivate_telnet()
        else:
            self.log.err(
                    "Did not understand NP_05B output %s" % (out))
            return False

    def _command(self, cmd):
        """ Send a command to the device """
        for n in range(self._num_tries):
            self._write(cmd)
            result = self.check_output(cmd)
            if result:
                return True
            else:
                continue
        return False

    def _deactivate_telnet(self):
        """ Attempt to deactivate Telnet session to the device """
        self.log.log("Telnet session active! Trying to deactivate...")
        cmd = '!'
        self._write(cmd)
        out = self._ser.readlines()[0]
        if cmd in out:
            return True
        else:
            self.log.err(
                    "Did not understand NP_05B output %s" % (out))
            return False
