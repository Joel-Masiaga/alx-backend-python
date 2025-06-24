
import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict

# Configure logging
logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(message)s')

# Task 1: Logging User Requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response


# Task 2: Restrict Chat Access by Time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        if request.path.startswith('/chats/'):
            # Allow access only between 6PM (18) and 9PM (21)
            if not (18 <= current_hour <= 21):
                return HttpResponseForbidden('Access to chat is restricted at this time.')

        response = self.get_response(request)
        return response


# Task 3: Detect and Block Offensive Language (Rate Limiting)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_times = defaultdict(list)

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chats/'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than 1 minute
            self.ip_message_times[ip] = [t for t in self.ip_message_times[ip] if now - t < timedelta(minutes=1)]

            if len(self.ip_message_times[ip]) >= 5:
                return HttpResponseForbidden('Message rate limit exceeded. Please wait a moment.')

            self.ip_message_times[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# Task 4: Enforce Chat User Role Permissions
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chats/'):
            user = request.user

            if not user.is_authenticated or user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden('You do not have permission to access this resource.')

        response = self.get_response(request)
        return response
