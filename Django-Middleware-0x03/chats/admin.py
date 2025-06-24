from django.contrib import admin
from .models import User, Conversation, Message

# Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'display_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')

# Register Conversation model
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    filter_horizontal = ('participants',)  # Makes it easy to add participants in the admin form

# Register Message model
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation', 'sender', 'sent_at')
    search_fields = ('message_body',)
    list_filter = ('sent_at',)
