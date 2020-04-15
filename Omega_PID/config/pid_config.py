# Configuration file for the Omega PID controller

# Information of the slowdaq aggregator
aggregator_ip = 'localhost'
aggregator_port = 3141

# IP and port of the PID controller, these should not need to change
PID_IP = '192.168.2.58'
PID_PORT = '2000'

# PID parameters for forwards (still need to find the correct values)
tune_p = 0.21
tune_i = 190
tune_d = 0

# PID parameters for backwards (still need to find the correct values)
stop_p = 0.19
stop_i = 170
stop_d = 0
