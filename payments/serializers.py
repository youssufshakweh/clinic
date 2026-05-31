from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'payment_id',
            'patient',
            'appointment',
            'nutritionist',
            'amount',
            'date',
            'time',
            'status',
            'type',
            'payment_method',
            'transaction_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['payment_id', 'created_at', 'updated_at']