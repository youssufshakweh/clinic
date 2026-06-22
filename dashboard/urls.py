from rest_framework import routers, urlpatterns

from .views import HomeViewSet

router = routers.DefaultRouter()

router.register(r'home', HomeViewSet, basename='home')

urlpatterns = router.urls