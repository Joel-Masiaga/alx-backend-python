from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from messaging.models import Message
from django.views.decorators.cache import cache_page

@cache_page(60)
@login_required
def conversation_view(request):
    messages = Message.unread.unread_for_user(request.user)
    return render(request, 'chats/conversation.html', {'messages': messages})

@login_required
def all_messages_view(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender')
    return render(request, 'chats/all_messages.html', {'messages': messages})

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'chats/delete_account.html')
