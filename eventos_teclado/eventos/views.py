from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import cv2
import threading
#import RPi.GPIO as GPIO
#from time import sleep
from django.views.decorators.gzip import gzip_page
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    x= 12
    direccion = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhB82XwnxSmPIer3V_bStkR-RqxlhFFcIc7GKoxX7NUXHt0N0S'
    return render(request,'eventos/index1.html')

#@csrf_exempt


def tecla_pre(request):
	if request.method == 'POST':
		
		tecla = request.POST.get('tecla_pre')
		print(tecla)
		response_data = {}
		response_data['tecla'] = tecla
		response_data['accion'] = 'presionada'
		if tecla == '74':
			#GPIO.output(7,True)
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		
	else:
        	return HttpResponse(
            	json.dumps({"nothing to see": "this isn't happening"}),
            	content_type="application/json"
       		)

def tecla_sol(request):
	if request.method == 'POST':
		
		tecla = request.POST.get('tecla_sol')
		print(tecla)
		response_data = {}
		response_data['tecla'] = tecla
		response_data['accion'] = 'soltada'
		if tecla == '74':
			#GPIO.output(7,False)
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		
		else:
		
  			return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


camera=VideoCamera()
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip_page
def video(request):
  
    return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    

