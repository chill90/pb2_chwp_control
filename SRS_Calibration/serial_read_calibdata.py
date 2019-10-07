#A script for retrieving calibration data from an already calibrated SIM922.
#Written by Samantha Rose Gilbert with assistanced from Dr. Mayuri Rao.
#October, 2017

import numpy as np
from scipy import loadtxt, optimize
import csv, sys
import serial 
import time
import matplotlib.pyplot as plt

SIM922="/dev/ttyUSB1" #Connect to the USB port on the computer where you have plugged in the mainframe (serial>USB).
ser=serial.Serial(port=SIM922,timeout=.1) #Set up the serial connection.

if __name__ == "__main__":
	try:

		ser.write('*IDN?\n\r') #Ping the mainframe for its identity to ensure you are connected. MUST END EVERY COMMAND WITH n\r to move 				                to the next line of commands.
		reply=ser.readlines() #Request a reply from the mainframe: should be "Stanford Research Systems SIM 900. . ."
		print reply

		ser.write("CONN 4, 'xyz'\n\r") #Connect to the SIM922 module sitting in slot 4 of the mainframe. Nonsense "xyz" exit string 					                CRUCIAL!
		ser.write('*IDN?\n\r') #Ping the module to ensure you are connected.
		reply=ser.readlines() #Request a reply from the mainframe: should be "Stanford Research Systems SIM 922. . ."
		print reply

		j=0 #Initialize number of data points for the loop.
		mylist=[] #Create a list in which to store the calibration data.
		while j < 162: #As long as we have not reached the last line of data,
			j += 1 #go to the next row of data,
			ser.write('CAPT? 1, %f\n\r' % j) #read the data from channel 1,
			time.sleep(.1)
			mylist.append(ser.readlines()) #and add it to a list.
			mylist.append('\n') #Create a new line in the list so that the next data row will be appended to the list there.
			#print mylist
			
		if reply == []:
			print "Not connected to SIM922" #If data isn't being read, here's how you'll know.
			ser.write('xyz\n\r')  #Nonsense escape string.
	
		
	except KeyboardInterrupt:
		ser.write('xyz\n\r')  #Nonsense escape string.

	calibration_data = mylist #Re-name the list of calibration data for the sake of specificity.
    	f = open('/home/akusaka/adr/ch1mainframe2check.txt', 'a') #Open a new text file in 'a'ppend mode (so that you don't over-write data with each execution 								  of the loop).
	
	for i in calibration_data: #Loop through the list to append the data to the new text file you just created.
		print_data = str #Convert the data to a string so that you can write to the text file using 'f.write'
       		f.write(str(i)) #Write to the text file
	f.close() #When finished, close the text file to be tidy.

    	
