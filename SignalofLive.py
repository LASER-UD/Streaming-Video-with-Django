import RPi.GPIO as GPIO
import os
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

response = 1
while response==1:
	response=os.system("ping -c 1 google.com &")
	sleep(1)

os.system("python3 /home/pi/Documents/Streaming-Video-with-Django/eventos_teclado/manage.py runserver 0:8000 &")

while True:
	
	response=os.system("ping -c 1 google.com &")

	
	if response==0:
		GPIO.output(7,True)
		sleep(0.5) 
		GPIO.output(7,False)
		sleep(0.5) 

	sleep(1)
