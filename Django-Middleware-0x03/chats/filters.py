import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name='sent_at')
    sender = django_filters.CharFilter(field_name='sender__email', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'created_at']
