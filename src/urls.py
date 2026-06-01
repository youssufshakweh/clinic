from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from subscriptions.views import PackageViewSet
from patients.views import PatientViewSet
from nutritionists.views import ProductViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)

router = DefaultRouter()
router.register('api/packages', PackageViewSet, basename='packages')
router.register('api/patients', PatientViewSet, basename='patients')
router.register('api/products', ProductViewSet, basename='products')


urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]


urlpatterns += router.urls