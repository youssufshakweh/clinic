from email.policy import default

from rest_framework import serializers

from appointments.constants import AppointmentType
from utils.constants import PercentageChangeDirection


class TrendSerializer(serializers.Serializer):
    total = serializers.IntegerField(default=0)
    current_month = serializers.IntegerField(default=0)
    previous_month = serializers.IntegerField(default=0)
    percentage_change = serializers.FloatField(default=0.0)
    direction = serializers.SerializerMethodField()

    def get_direction(self, obj):
        percentage_change = obj['percentage_change']

        if not percentage_change:
            return PercentageChangeDirection.NO_CHANGE.value
        
        if percentage_change > 0:
            return PercentageChangeDirection.INCREASE.value
        
        return PercentageChangeDirection.DECREASE.value


class ProductProfitTrendSerializer(TrendSerializer):
    total = serializers.FloatField()
    current_month = serializers.FloatField()
    previous_month = serializers.FloatField()


class TodayAppointmentsSerializer(serializers.Serializer):
    incoming = serializers.IntegerField(default=0)
    upcoming = serializers.IntegerField(default=0)


class CardSerializer(serializers.Serializer):
    today = TodayAppointmentsSerializer(read_only=True)
    subscribers_trend = TrendSerializer(read_only=True)
    incoming_queries = serializers.IntegerField(read_only=True)
    product_profit_trend = ProductProfitTrendSerializer(read_only=True)
    count_of_low_stock_products = serializers.IntegerField()
    cancelled_trend = TrendSerializer(read_only=True)


class AppointmentStatsQuerySerializer(serializers.Serializer):
    groupby = serializers.ChoiceField(choices=['weekday', 'month', 'year'], default='weekday')
    type = serializers.ChoiceField(choices=[AppointmentType.ONLINE.value, AppointmentType.IN_PERSON.value], required=False)
    year = serializers.IntegerField(required=False, allow_null=True)
    month = serializers.IntegerField(required=False, allow_null=True)
    week = serializers.IntegerField(required=False, allow_null=True)


class PeakBookingDaySerializer(serializers.Serializer):
    day_id = serializers.IntegerField()
    day_name = serializers.CharField()


class AppointmentDistributionSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    counts = serializers.ListField(child=serializers.IntegerField())


class AppointmentStatsSerializer(serializers.Serializer):
    completed_appointments = serializers.IntegerField()
    peak_booking_day = PeakBookingDaySerializer()
    appointment_distribution = AppointmentDistributionSerializer()