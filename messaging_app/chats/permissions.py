from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants in the conversation.
    Also restricts unsafe methods (PUT, PATCH, DELETE) to participants only.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user not in obj.participants.all():
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.all()

        return True
