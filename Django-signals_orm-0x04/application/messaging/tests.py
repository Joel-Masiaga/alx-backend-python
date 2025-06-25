from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_signal_creates_notification(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        self.assertTrue(Notification.objects.filter(user=self.receiver, message=msg).exists())

    def test_message_edit_creates_history(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Original')
        msg.content = 'Updated'
        msg.save()
        self.assertTrue(MessageHistory.objects.filter(message=msg, old_content='Original').exists())
