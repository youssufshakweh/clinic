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

from .serializers import (
    CardSerializer,
    AppointmentStatsQuerySerializer,
    AppointmentStatsSerializer,
    ProductStatsSerializer
)

class HomeViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdminUser]

    @extend_schema(responses={200: CardSerializer})
    @action(detail=False, methods=['get'])
    def overview(self, request: Request) -> Response:
        data = self._get_data()
        serializer = CardSerializer(data)
        return Response(serializer.data)

    @extend_schema(
        parameters=[AppointmentStatsQuerySerializer],
        responses={200: AppointmentStatsSerializer}
    )
    @action(detail=False, methods=['get'])
    def appointment_stats(self, request: Request) -> Response:
        query_serializer = AppointmentStatsQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        
        data = self._get_appointment_stats_data(query_serializer.validated_data)
        serializer = AppointmentStatsSerializer(data)
        return Response(serializer.data)

    @extend_schema(responses={200: ProductStatsSerializer})
    @action(detail=False, methods=['get'])
    def product_stats(self, request: Request) -> Response:
        data = self._get_product_stats_data()
        serializer = ProductStatsSerializer(data)
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

    def _get_appointment_stats_data(self, validated_data: dict) -> dict:
        groupby = validated_data.get('groupby', 'weekday')
        appointment_type = validated_data.get('type')
        year = validated_data.get('year')
        month = validated_data.get('month')
        week = validated_data.get('week')
        
        total_completed = app_selectors.get_total_completed_appointments(appointment_type)
        peak_booking_day = app_selectors.get_most_booking_weekday(appointment_type)
        distribution_data = app_selectors.get_appointments_by_period(
            groupby=groupby,
            appointment_type=appointment_type,
            year=year,
            month=month,
            week=week
        )
        
        labels, counts = self._format_distribution_data(groupby, distribution_data)
        
        return {
            'completed_appointments': total_completed,
            'peak_booking_day': peak_booking_day,
            'appointment_distribution': {
                'labels': labels,
                'counts': counts
            }
        }

    def _format_distribution_data(self, groupby: str, distribution_data: list) -> tuple[list[str], list[int]]:
        if groupby == 'weekday':
            labels = [item['day_name'] for item in distribution_data]
            counts = [item['count'] for item in distribution_data]
        elif groupby == 'month':
            labels = [item['month_name'] for item in distribution_data]
            counts = [item['count'] for item in distribution_data]
        elif groupby == 'year':
            labels = [str(item['year']) for item in distribution_data]
            counts = [item['count'] for item in distribution_data]
        else:
            labels = []
            counts = []
        
        return labels, counts

    def _get_product_stats_data(self) -> dict:
        best_selling_product = pay_selectors.get_best_selling_product()
        revenue_distribution = pay_selectors.get_product_revenue_distribution()
        
        return {
            'best_selling_product': best_selling_product,
            'revenue_distribution': revenue_distribution
        }