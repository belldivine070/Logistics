from django.urls import path
from .views import (
    AdminSupportInboxView,
    AdminChatRoomView,
)

urlpatterns = [
    # Staff Support Dashboard
    path('dashboard/inbox/', AdminSupportInboxView.as_view(), name='admin_support_inbox'),
    path('dashboard/chat/<str:conversation_id>/', AdminChatRoomView.as_view(), name='admin_chat_room'),
]