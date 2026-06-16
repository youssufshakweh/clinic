from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, AvailableSlotsView, BookAppointmentView, AppointmentListView

router = DefaultRouter()
router.register('schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('book/', BookAppointmentView.as_view(), name='appointment-book'),
    path('available-slots/', AvailableSlotsView.as_view(), name='available-slots'),
    path('', include(router.urls)),
]
