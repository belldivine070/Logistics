from django.db import models
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


class ChatConversation(models.Model):
    conversation_id = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='support_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat {self.conversation_id}"


class ChatMessage(models.Model):
    SENDER_TYPES = [
        ('CUSTOMER', 'Customer'),
        ('SUPPORT', 'Support Staff'),
    ]
    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPES, default='CUSTOMER')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.sender_type}] {self.message[:30]}"



@receiver(user_logged_in)
def migrate_guest_chat_on_login(sender, request, user, **kwargs):
    """
    Automatically reassigns any active guest chat session tied to the browser cookie
    to the newly authenticated user upon successful login.
    """
    guest_chat_id = request.COOKIES.get('guest_chat_id')
    if guest_chat_id:
        try:
            # Find the guest conversation using ChatConversation and bind it to the logged-in customer
            conversation = ChatConversation.objects.get(conversation_id=guest_chat_id, customer__isnull=True)
            conversation.customer = user
            conversation.save()
        except ChatConversation.DoesNotExist:
            pass