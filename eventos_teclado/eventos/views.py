from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import cv2
import threading
#import RPi.GPIO as GPIO
#from time import sleep

from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
# Create your views here.

# def chat(request):
#     return render(request, 'eventos/chat.html', {})

# def room(request, room_name):
#     return render(request, 'eventos/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))
#     })

@login_required
def index(request):
    return render(request,'eventos/index1.html')

#@csrf_exempt


