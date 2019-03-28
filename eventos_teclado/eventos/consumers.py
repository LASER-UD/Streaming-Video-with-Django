from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import base64
import cv2
import threading
import time
import serial
import threading

class SerialD():
    cuenta=0
    def __init__(self):
         self.datos=None;
         self.ser = serial.Serial()
         self.ser.baudrate = 115200
         self.ser.port = '/dev/ttyACM0'

    def start(self):
         self.ser.open()
    def end(self):
         self.ser.close()
    def update(self):
        self.ser.write(b"g")
        self.ser.flush() #espera a  exista un dato
        self.datos=int(self.ser.readline())
        return self.datos 
        
class VideoCamera(object):
    clientes=0;
    image=None;
    def start(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
    def end(self):
        self.video.release()

    def get_frame(self):
        (self.grabbed, self.frame) = self.video.read()
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        
    

camera = VideoCamera()
seri= SerialD()

#asincrono
#https://channels.readthedocs.io/en/latest/tutorial/part_3.html explicacion de como usar 

class webcam(WebsocketConsumer):

    
    def connect(self):
        
        self.room_group_name = 'webcam'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        camera.clientes=camera.clientes + 1
        print(camera.clientes)

        if(camera.clientes==1):
            camera.start()
            seri.start()
            self.tiempo1()
        
        async_to_sync(self.send(text_data=json.dumps({
                'type':'clientes',
                'message': camera.clientes
            })))
        
    def disconnect(self, close_code):
        # Leave room group
        camera.clientes=camera.clientes -1
        if(camera.clientes==0):
            camera.end()
            seri.end()
            time1.cancel()
            async_to_sync (self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            ))
        else:
            async_to_sync (self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': 'desc',
                    'tipo': 'clientes'
                }
            ))
            
        print(camera.clientes)
        
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if text_data_json['tipo']=='tecla':
            print(str(message)+ text_data_json['accion'])
        
    # Receive message from room group
    def chat_message(self, event):
        tipo = event['tipo']
        if(tipo=='imagen'):
            async_to_sync( self.send(text_data=json.dumps({'type':tipo,'message':base64.b64encode(camera.get_frame()).decode('ascii')})))
        else:
            async_to_sync( self.send(text_data=json.dumps({'type':tipo})))
    def tiempo1(self):
        
        self.update()
        timer1 = threading.Timer(0.016,self.tiempo2)
        timer1.start()
        
    def tiempo2(self):
        self.update()
        timer2 = threading.Timer(0.016,self.tiempo1)
        timer2.start()
            
    def update(self):
        if (seri.cuenta==10):
               seri.cuenta=0
        else:
               seri.cuenta=seri.cuenta+1
        async_to_sync( self.send(text_data=json.dumps({'type':'imagen','message':base64.b64encode(camera.get_frame()).decode('ascii')})))

        
        
        
