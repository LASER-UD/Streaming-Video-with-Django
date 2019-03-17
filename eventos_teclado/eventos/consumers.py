from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import base64
import cv2
import threading
import time
class VideoCamera(object):
    def start(self):
        self.cliente = False
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def end(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while self.video.read():
            (self.grabbed, self.frame) = self.video.read()

camera = VideoCamera()
#sincrono
class ChatConsumer(WebsocketConsumer):
    frame=None
    clientes=0
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        if(self.clientes==0):
            camera.start()
            self.clientes=self.clientes+1
        else:
            self.clientes=self.clientes+1
        print(self.clientes)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.clientes=self.clientes-1
        if(self.clientes==0):
            camera.end()
        print(self.clientes)

    # Receive message from WebSocket
    def receive(self, text_data):
        self.frame=base64.b64encode(camera.get_frame())
        self.send(text_data=self.frame.decode('ascii'))
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )
       


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        if message=='1':
            self.frame=base64.b64encode(camera.get_frame())
            self.send(text_data=self.frame.decode('ascii'))
        else:    
            self.send(text_data=json.dumps({
                'type':'mensaje',
                'message': message
            }))

  


#asincrono
#https://channels.readthedocs.io/en/latest/tutorial/part_3.html explicacion de como usar 

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer1(AsyncWebsocketConsumer):
    frame=None
    clientes=0
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        if(self.clientes==0):
             self.clientes=self.clientes+1
             threading.Thread(target=self.gen(camera), args=()).start()
        else:
             self.clientes=self.clientes+1
             print(self.clientes)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        self.clientes=self.clientes-1
        print(self.clientes)


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
             'type':'mensaje',
            'message': message
        }))

    def gen(self,camera):
        camera.start();
        while True:
            if self.clientes>0:
                self.frame =base64.b64encode(camera.get_frame())
                self.send(text_data=self.frame)
            else:
                camera.end()
                break