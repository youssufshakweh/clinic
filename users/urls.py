from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

from .views import VerifyEmailView

urlpatterns = [
    path('users/verify_email/', VerifyEmailView.as_view(), name='verify-email'),
    path('', include(router.urls)),
]
