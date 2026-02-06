from django.urls import re_path
from .consumers import GameConsumer

# definimos para todas las rutas websocket
websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_name>\w+)/$', GameConsumer.as_asgi()),
]