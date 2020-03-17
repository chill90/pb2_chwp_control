# Built-in python modules
import time as tm
import serial as sr
import sys as sy
import os

# CHWP Control modules
this_dir = os.path.dirname(__file__)
sy.path.append(os.path.join(
    this_dir, "..", "..", "MOXA"))
import moxaSerial as mx  # noqa: E402

class PMX:
    """
    The PMX object is for communicating with the Kikusui PMX power supplies

    Args:
    rtu_port (str): Serial RTU port
    tcp_ip (str): TCP IP address
    tcp_port (int): TCP port
    """
    def __init__(self, rtu_port=None, tcp_ip=None, tcp_port=None):
        # Connect to device
        msg = self.__conn(rtu_port, tcp_ip, tcp_port)
        print(msg)
        self._remote_Mode()

        # Timing variables
        self._tstep = 0.1  # sec

    def __del__(self):
        if not self.using_tcp:
            print(
                "Disconnecting from RTU port %s"
                % (self._rtu_port))
            self.ser.close()
        else:
            print(
                "Disconnecting from TCP IP %s at port %d"
                % (self._tcp_ip, self._tcp_port))
            pass
        return

    def check_voltage(self):
        """ Check the voltage """
        self.clean_serial()
        bts = self.ser.write(str.encode("MEAS:VOLT?\n\r"))
        self.wait()
        val = float(self.ser.readline())
        msg = "Measured voltage = %.3f V" % (val)
        print(msg)
        return msg, val

    def check_current(self):
        """ Check the current """
        self.clean_serial()
        self.ser.write(str.encode("MEAS:CURR?\n\r"))
        self.wait()
        val = float(self.ser.readline())
        msg = "Measured current = %.3f A" % (val)
        print(msg)
        return msg, val

    def check_voltage_current(self):
        """ Check both the voltage and current """
        self.clean_serial()
        voltage = self.check_voltage()[1]
        current = self.check_current()[1]
        msg = (
            "Measured voltage = %.3f V\n"
            "Measured current = %.3f A\n"
            % (voltage, current))
#        print(msg)
        return voltage, current

    def check_output(self):
        """ Return the output status """
        self.clean_serial()
        self.ser.write(str.encode("OUTP?\n\r"))
        self.wait()
        val = int(self.ser.readline())
        if val == 0:
            msg = "Measured output state = OFF"
        elif val == 1:
            msg = "Measured output state = ON"
        else:
            msg = "Failed to measure output..."
        print(msg)
        return msg, val

    def set_voltage(self, val):
        """ Set the PMX voltage """
        self.clean_serial()
        self.ser.write(str.encode("VOLT %f\n\r" % (float(val))))
        self.wait()
        self.ser.write(str.encode("VOLT?\n\r"))
        self.wait()
        val = self.ser.readline()
        msg = "Voltage set = %.3f V" % (float(val))
        print(msg)

        return msg

    def set_current(self, val):
        """ Set the PMX on """
        self.clean_serial()
        self.ser.write(str.encode("CURR %f\n\r" % (float(val))))
        self.wait()
        self.ser.write(str.encode("CURR?\n\r"))
        self.wait()
        val = self.ser.readline()
        msg = "Current set = %.3f A\n" % (float(val))
        print(msg)

        return msg

    def turn_on(self):
        """ Turn the PMX on """
        self.clean_serial()
        self.ser.write(str.encode("OUTP ON\n\r"))
        self.wait()
        self.ser.write(str.encode("OUTP?\n\r"))
        self.wait()
        val = self.ser.readline()
        msg = "Output state = %s" % (val)
        print(msg)

        return msg

    def turn_off(self):
        """ Turn the PMX off """
        self.clean_serial()
        self.ser.write(str.encode("OUTP OFF\n\r"))
        self.wait()
        self.ser.write(str.encode("OUTP?\n\r"))
        self.wait()
        val = self.ser.readline()
        msg = "Output state = %s" % (val)
        print(msg)

        return msg

    # ***** Helper Methods *****
    def __conn(self, rtu_port=None, tcp_ip=None, tcp_port=None):
        """
        Connect to the PMX module

        Args:
        rtu_port (str): Serial RTU port
        tcp_ip (str): TCP IP address
        tcp_port (int): TCP port
        """
        if rtu_port is None and (tcp_ip is None or tcp_port is None):
            raise Exception(
                "Aborted PMX._conn() due to no RTU or "
                "TCP port specified")
        elif (rtu_port is not None and
              (tcp_ip is not None or tcp_port is not None)):
            raise Exception(
                "Aborted PMX._conn() due to RTU and TCP port both being "
                "specified. Can only have one or the other.")
        elif rtu_port is not None:
            self.ser = sr.Serial(
                port=rtu_port, baudrate=19200, bytesize=8,
                parity='N', stopbits=1, timeout=1)
            self._rtu_port = rtu_port
            self.using_tcp = False
            msg = "Connected to RTU port %s" % (rtu_port)
        elif tcp_ip is not None and tcp_port is not None:
            self.ser = mx.Serial_TCPServer((tcp_ip, tcp_port))
            self._tcp_ip = tcp_ip
            self._tcp_port = int(tcp_port)
            self.using_tcp = True
            msg = "Connected to TCP IP %s at port %d" % (tcp_ip, tcp_port)
        else:
            raise Exception(
                "Aborted PMX._conn() due to unknown error")
        return msg

    def wait(self):
        """ Sleep """
        tm.sleep(0.1)
        return True

    def clean_serial(self):
        """ Flush the serial buffer """
        if not False:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.ser.flush()
        else:
            self.ser.flushInput()
        return True

    def _remote_Mode(self):
        """ Enable remote control """
        self.clean_serial()
        self.ser.write(str.encode('SYST:REM\n\r'))
        self.wait()
        return True
