from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from subscriptions.views import PackageViewSet
from patients.views import PatientViewSet
from nutritionists.views import ProductViewSet

router = DefaultRouter()
router.register('api/packages', PackageViewSet, basename='packages')
router.register('api/patients', PatientViewSet, basename='patients')
router.register('api/products', ProductViewSet, basename='products')


urlpatterns = [
    path('admin/', admin.site.urls),
]
