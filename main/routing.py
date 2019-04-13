# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/party/1/1', consumers.ChatConsumer),
]
