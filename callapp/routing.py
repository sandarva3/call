from django.urls import path
from callapp.consumers import SignalingConsumer

websocket_urlpatterns = [
    path('ws/signaling/', SignalingConsumer.as_asgi()),
]
