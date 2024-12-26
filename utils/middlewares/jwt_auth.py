import pprint
import jwt
from django.conf import settings
from django.http import JsonResponse
from apps.users.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated


class JWTAuthenticationMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude paths that should not be authenticated
        excluded_paths = ['/api/login/', '/api/token/refresh/','/api/signup/', '/api/forgot-password/','/api/admin/']
        
        # If the request path is excluded, skip authentication
        if request.path in excluded_paths:
            return self.get_response(request)

        if IsAuthenticated():
            return self.get_response(request)
        else:
            return JsonResponse({"detail": "Invalid token"}, status=401)