from django.urls import path
from . import views

app_name='eventos'
urlpatterns=[
   path('',views.index,name='index'),
   path('tecla_pre/',views.tecla_pre,name='tecla_pre'),
   path('tecla_sol/',views.tecla_sol,name='tecla_sol'),
   path('video/',views.video,name='video'),
   path('chat/',views.chat, name='chat'),
   path('chat/<slug:room_name>/',views.room,name='room')
]
