from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'participants__username'] 
    ordering_fields = ['created_at']  
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        participants_ids = request.data.get('participants', [])

        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(participants_ids, list) or not participants_ids:
            return Response({'error': 'Participants must be a non-empty list of user IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participants_ids)

        if not participants.exists():
            return Response({'error': 'No valid participants found.'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create(title=title)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        conversation = self.get_object()
        sender = request.user
        message_body = request.data.get('message_body')

        if not message_body:
            return Response({'error': 'message_body is required'}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    pagination_class = MessagePagination

    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)