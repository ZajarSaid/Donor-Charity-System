from django.contrib import admin

# Register your models here.
from .models import ConversationMessage, Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('created_at',)
    filter_horizontal = ('members',)

@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('message', 'created_by__username', 'conversation__id')