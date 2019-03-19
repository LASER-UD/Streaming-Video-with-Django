from django.urls import path
from . import views

app_name='eventos'
urlpatterns=[
   path('',views.index,name='index'),
]
