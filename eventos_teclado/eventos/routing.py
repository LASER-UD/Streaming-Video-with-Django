from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/eventos/chat/<slug:room_name>/', consumers.ChatConsumer),
]