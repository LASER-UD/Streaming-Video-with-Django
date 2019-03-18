from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import base64
import cv2
import threading
import time
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

    def update(self):
        while self.video.read():
            (self.grabbed, self.frame) = self.video.read()


camera = VideoCamera()

#sincrono
class ChatConsumer1(WebsocketConsumer):
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        
        self.send(text_data=json.dumps({
                'type':'clientes',
                'message': camera.clientes
            }))
        
    def disconnect(self, close_code):
        # Leave room group
        
        camera.clientes=camera.clientes -1
        if(camera.clientes==0):
            camera.end()
            async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': 'desc',
                'tipo': 'clientes'
            }
            )
            
        print(camera.clientes)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'tipo': 'mensaje',
            }
        )


    def chat_message(self, event):
        message = event['message']
        tipo = event['tipo']
        if(message=='1'):
            self.send(text_data=json.dumps({'type':'imagen','message':base64.b64encode(camera.get_frame()).decode('ascii')}))
        else:
            self.send(text_data=json.dumps({'type':tipo,'message':message}))
            
    
       

#asincrono
#https://channels.readthedocs.io/en/latest/tutorial/part_3.html explicacion de como usar 

from channels.generic.websocket import AsyncWebsocketConsumer

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
        
        await self.send(text_data=json.dumps({
                'type':'clientes',
                'message': camera.clientes
            }))
        

    async def disconnect(self, close_code):
        # Leave room group
        camera.clientes=camera.clientes -1
        if(camera.clientes==0):
            camera.end()
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
            print(message)
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'tipo': 'mensaje'
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        tipo = event['tipo']
        if(message=='1'):
            await self.send(text_data=json.dumps({'type':'imagen','message':base64.b64encode(camera.get_frame()).decode('ascii')}))
        else:
            await self.send(text_data=json.dumps({'type':tipo,'message':message}))
   
class tecla(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.room_group_name = 'tecla'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        

    async def disconnect(self, close_code):
        # Leave room group
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)