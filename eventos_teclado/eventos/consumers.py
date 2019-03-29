from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64
import cv2
import threading
import time
import serial

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
     def press(self,key):
         print(key.encode('cp1250'))
         self.ser.write(key.encode('cp1250'))#codifica y envia
        
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

class webcam(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.room_group_name = 'webcam'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        camera.clientes=camera.clientes + 1
        print(camera.clientes)

        if(camera.clientes==1):
            camera.start()
            seri.start()
        
        await self.send(text_data=json.dumps({
                'type':'clientes',
                'message': camera.clientes
            }))
        

    async def disconnect(self, close_code):
        # Leave room group
        camera.clientes=camera.clientes -1
        if(camera.clientes==0):
            camera.end()
            seri.end()
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': 'desc',
                    'tipo': 'clientes'
                }
            )
            
        print(camera.clientes)
        


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if text_data_json['tipo']=='tecla':
            seri.press(str(message))
        else: #imagen
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'tipo': text_data_json['tipo'],
                    'message':''
                }
            )
            if (seri.cuenta==10):
                seri.update()# Actualiza
#               await self.channel_layer.group_send(
#                    self.room_group_name,
#                    {
#                        'type': 'chat_message',
#                        'tipo': 'data'
#                    }
#                )
                seri.cuenta=0
            else:
                seri.cuenta=seri.cuenta+1

    # Receive message from room group
    async def chat_message(self, event):
        tipo = event['tipo']
        if(tipo=='imagen'):
            await self.send(text_data=json.dumps({'type':tipo,'message':base64.b64encode(camera.get_frame()).decode('ascii')}))
        else:
            await self.send(text_data=json.dumps({'type':tipo,'message': event['message']}))
