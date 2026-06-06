from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from subscriptions.views import PackageViewSet, WorkshopViewSet
from publications.views import PublicationViewSet
from patients.views import PatientViewSet
from nutritionists.views import ProductViewSet
from users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)

from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)


router = DefaultRouter()
router.register('api/packages', PackageViewSet, basename='packages')
router.register('api/patients', PatientViewSet, basename='patients')
router.register('api/products', ProductViewSet, basename='products')
router.register('api/users', UserViewSet, basename='users')
router.register('api/workshop', WorkshopViewSet, basename='workshops')
router.register('api/publications', PublicationViewSet, basename='publications')

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Contact
    path('api/contact/', include('contact.urls')),

    # Optional UI:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


urlpatterns += router.urls