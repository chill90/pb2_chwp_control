import src.pmx       as pm
import time          as tm
import numpy         as np
import sys           as sy
import datetime      as dt

import config.config as cg

#************ Main *************

args = sy.argv[1:]
if not len(args) == 1:
    sy.exit("\nUsage: python loadCurve.py [runName]\n")
else:
    runName = args[0]

#File to write to
fname = 'Data/%s.txt' % (runName)
def write(msg):
    now = dt.datetime.now()
    f = open(fname, 'a+')
    mg = "[%04d-%02d-%02d %02d:%02d:%02d] %s\n" % (now.year, now.month, now.day, now.hour, now.minute, now.second, msg)
    f.write(mg)
    f.close()
    return True

#Parameters for the test
R = 24.0 #Ohms
powers = np.array([6., 9.])
voltages = np.sqrt(R*powers) #V
#Times in hours, 3600 sec per hour
times = np.array([4.]*len(voltages))*3600.
if len(times) != len(voltages):
    raise Exception ("Problem with the times array!")

#Initialize serial connection to the Kikusui
pmx = pm.PMX(cg.port)

#Step the voltage
for i in range(len(times)):
    t = times[i]
    v = voltages[i]
    #Set the voltage
    write("Setting voltage = %.02f V" % (v))
    pmx.setVoltage(v)
    if not i:
        pmx.turnOn()
    tm.sleep(2)
    c = pmx.checkCurrent()
    write("Checking initial current = %.03f A" % (float(c)))
    write("Checking initial power   = %.03f W" % (float(c)*float(v)))
    tm.sleep(t)
    c = pmx.checkCurrent()
    write("Checking final current = %.03f A" % (float(c)))
    write("Checking final power   = %.03f W" % (float(c)*float(v)))
    write('\n')

pmx.turnOff()
print "Done"
