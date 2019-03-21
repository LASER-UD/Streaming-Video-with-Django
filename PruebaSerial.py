import time
import serial
ser = serial.Serial('/dev/ttyACM0',115200)    # enable the serial port
data ="" 
while 1:                                                             # execute the loop forever
		while ser.inWaiting() > 0: #espera a que exista un dato
			data=ser.readline()
			print (data)
