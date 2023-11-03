from django.urls import re_path, path

from .consumers import StoneStatusConsumer

websocket_urlpatterns = [
    path(
        "ws/ac/stone_status",StoneStatusConsumer.as_asgi()
    ),
]
