import os
import django

# 1. Set settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# 2. Initialize Django setup explicitly before importing any app modules or routing
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import support.routing

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            support.routing.websocket_urlpatterns
        )
    ),
})