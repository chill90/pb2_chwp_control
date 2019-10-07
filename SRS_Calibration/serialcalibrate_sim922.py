#A script to calibrate the SIM922 Diode Temperature Module in the SIM900 Mainframe by communicating via serial.
#Written by Samantha Rose Gilbert with assistance from Dr. Mayuri Rao
#October, 2017

import numpy as np
from scipy import loadtxt, optimize
import csv, sys
import serial 
import time
import matplotlib.pyplot as plt

SIM922="/dev/ttyUSB1" #Connect to the USB port on the computer where you have plugged in the mainframe (serial>USB).
ser=serial.Serial(port=SIM922,timeout=.1) #Set up the serial connection.

v1,t1 = loadtxt('/home/akusaka/adr/ch1calibdata.txt', unpack=True) #The 161 calibration data points sit in text files in the adr folder. 
								   #Upload the data from the text files, where the first column is voltages and 								    the second column is temperatures. 
v2,t2 = loadtxt('/home/akusaka/adr/ch2calibdata.txt', unpack=True) #There is one file corresponding to each channel on the original mainframe.
								   
v3,t3 = loadtxt('/home/akusaka/adr/ch3calibdata.txt', unpack=True)

if __name__ == "__main__":
	try:

		ser.write("*IDN?\n\r") #Ping the mainframe for its identity to ensure you are connected. MUST END EVERY COMMAND WITH n\r to move 				                to the next line of commands.
		reply=ser.readlines() #Request a reply from the mainframe: should be "Stanford Research Systems SIM 900. . ."
		print reply

		ser.write("CONN 5, 'xyz'\n\r") #Connect to the SIM922 module sitting in slot 4 of the mainframe. Nonsense "xyz" exit string 					                CRUCIAL!
		ser.write("*IDN?\n\r") #Ping the module to ensure you are connected.
		reply=ser.readlines() #Request a reply from the mainframe: should be "Stanford Research Systems SIM 922. . ."
		print reply

		ser.write("CINI 1,0,DT670a\n\r") #Initialize calibration. First number is channel on SIM922 (1-4), second is "LINEAR" curve type (see SIM922 							manual), third is a string with an identifying name of your choosing. DT670 refers to our Silicon diode 	  					thermometers from Lakeshore.
		ser.write("CURV 1,1\n\r") #Tell the module we are about to upload a calibration curve. First number is channel on SIM922 (1-4), second is 						   USER-selected curve (as opposed to STANDARD - 0).

		for i in range(0,np.size(v2)):	#This loop will go through each row of calibration data (V, T) and upload it to channel you chose above.
			print i, v2[i], t2[i]	#Report the number of data points to make sure all 161 get uploaded (remember Python starts at i=0).	
			ser.write("CAPT 1, %f, %f\n\r" % (v2[i], t2[i])) #Upload calibration points to channel 4, x=Voltage v, y = Temperature t.
			time.sleep(.5)
			
		if reply == []:
			print "Not connected to SIM922" #If data isn't uploading, here's how you'll know.
			ser.write('xyz\n\r') #Nonsense escape string.
		
		ser.write('xyz\n\r') #Nonsense escape string.
		
		ser.write("CURV 1,1\n\r") #Tell the module we are about to upload a calibration curve. First number is channel on SIM922 (1-4), second is 						   USER-selected curve (as opposed to STANDARD - 0).
	except KeyboardInterrupt:
		ser.write('xyz\n\r') #Nonsense escape string.

