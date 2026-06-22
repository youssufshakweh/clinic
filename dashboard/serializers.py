from email.policy import default

from rest_framework import serializers

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