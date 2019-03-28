import threading
import time

def gfg1():
	print('hola 1')
	timer1 = threading.Timer(1,gfg2)
	timer1.start()	
	
def gfg2():
	print('hola 2')
	timer2 = threading.Timer(1,gfg1)
	timer2.start()

timer1 = threading.Timer(1,gfg2)
timer1.start()			
while True:
	print('Q')
	time.sleep(1)
