from django.urls import path
from .views import SignupView, ForgotPasswordView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
