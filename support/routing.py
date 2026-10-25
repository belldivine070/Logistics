from django.urls import re_path
from .consumers import SupportChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>[\w-]+)/$', SupportChatConsumer.as_asgi()),
]