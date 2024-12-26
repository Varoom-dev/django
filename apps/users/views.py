from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from .models import User
from .serializers import SignupSerializer, UserSerializer, PasswordResetSerializer, PasswordChangeSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]
    # Use DRF JWT Token Authentication

class ForgotPasswordView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = PasswordResetTokenGenerator().make_token(user)
                send_mail(
                    'Password Reset Request',
                    f'Use the token {token} to reset your password.',
                    'from@example.com',
                    [email],
                )
            return Response({'message': 'Password reset email sent.'})
        return Response(serializer.errors, status=400)

class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
