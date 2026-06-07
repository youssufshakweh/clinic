from django.urls import path

from .views import VerifyEmailView

urlpatterns = [
    path('users/verify_email/', VerifyEmailView.as_view(), name='verify-email'),
]
