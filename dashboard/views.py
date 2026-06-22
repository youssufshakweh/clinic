from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from appointments import selectors as app_selectors
from contact import selectors as cont_selectors
from nutritionists import selectors as nut_selectors
from patients import selectors as pat_selectors
from payments import selectors  as pay_selectors
from utils.math import calculate_percentage_change

from .serializers import CardSerializer

class HomeViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]

    @extend_schema(responses={200: CardSerializer})
    @action(detail=False, methods=['get'])
    def overview(self, request: Request) -> Response:
        data = self._get_data()
        serializer = CardSerializer(data)
        return Response(serializer.data)

    def _get_data(self):
        return {
            'today': self._get_today_appointments_stats(),
            'subscribers_trend': self._get_subscribtion_trend(),
            'cancelled_trend': self._get_cancelled_appointments_trend(),
            'incoming_queries': cont_selectors.get_unread_inquiries_count(),
            'count_of_low_stock_products': nut_selectors.get_count_of_low_stock_product(),
            'product_profit_trend': self._get_product_profit_trend()
        }

    def _get_today_appointments_stats(self) -> dict:
        incoming = app_selectors.get_incoming_appointments_for_today_count()
        upcoming = app_selectors.get_upcoming_appointments_for_today_count()

        return {
            "incoming": incoming,
            "upcoming": upcoming
        }

    def _get_subscribtion_trend(self):
        total = pat_selectors.get_total_patients_count()
        curr_month = pat_selectors.get_total_patients_count_for_current_month()
        prev_month = pat_selectors.get_total_patients_count_for_previous_month()

        return {
            "total": total,
            "current_month": curr_month,
            "previous_month": prev_month,
            "percentage_change": calculate_percentage_change(curr_month, prev_month)
        }

    def _get_cancelled_appointments_trend(self) -> dict:
        total = app_selectors.get_total_cancelled_appointments()
        curr_month = app_selectors.get_total_cancelled_appointments_for_current_month()
        prev_month = app_selectors.get_total_cancelled_appointments_for_previous_month()

        return {
            "total": total,
            "current_month": curr_month,
            "previous_month": prev_month,
            "percentage_change": calculate_percentage_change(curr_month, prev_month)
        }

    def _get_product_profit_trend(self) -> dict:
        total = pay_selectors.get_total_product_profit()
        curr_month = pay_selectors.get_total_product_profit_for_current_month()
        prev_month = pay_selectors.get_total_product_profit_for_previous_month()

        return {
            "total": total,
            "current_month": curr_month,
            "previous_month": prev_month,
            "percentage_change": calculate_percentage_change(curr_month, prev_month)
        }