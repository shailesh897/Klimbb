import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import stones_app 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infinity_stones.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(stones_app.routing.websocket_urlpatterns),
    }
)
