from django.views.generic import ListView, DetailView
from core.mixins import StaffRequiredMixin
from .models import ChatConversation

class AdminSupportInboxView(StaffRequiredMixin, ListView):
    model = ChatConversation
    template_name = 'dashboard/support_inbox.html'
    context_object_name = 'conversations'
    ordering = ['-updated_at']


class AdminChatRoomView(StaffRequiredMixin, DetailView):
    model = ChatConversation
    template_name = 'support/chat_room.html'
    context_object_name = 'conversation'
    slug_field = 'conversation_id'
    slug_url_kwarg = 'conversation_id'