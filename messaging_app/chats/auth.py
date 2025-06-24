from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    This view can be used to customize token responses in the future.
    """
    pass

def get_tokens_for_user(user):
    """
    Utility function to generate JWT tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
