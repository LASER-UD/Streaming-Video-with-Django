import time
import serial
ser = serial.Serial('/dev/ttyACM0',115200)    # enable the serial port
data ="" 

while 1:    
	time.sleep(1)
	ser.write(b"g")                                                
	ser.flush() #espera a que exista un dato
	data=ser.readline()
	print (int(data))
