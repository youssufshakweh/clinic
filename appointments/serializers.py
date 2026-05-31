from rest_framework import serializers
from .models import Appointment
from patients.models import Patient
from nutritionists.models import Nutritionist

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'app_id',
            'patient',
            'nutritionist',
            'date',
            'time',
            'status',
            'type',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['app_id', 'created_at', 'updated_at']
