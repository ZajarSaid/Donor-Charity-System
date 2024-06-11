from django.db import models
from users.models import CustomUser
# Create your models here.

class Conversation(models.Model):
    members = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation started at {self.created_at}"

    class Meta:
        verbose_name_plural = 'Conversation'
        ordering = ('-modified_at',)


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, related_name='user_messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message by {self.created_by} on {self.created_at}"

