from rest_framework import serializers
from .models import Clinic

class ClinicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Clinic
        fields = [
            'clinic_id', 'name', 'email', 'phone', 'logo',
            'latitude', 'longitude', 'created_at', 'updated_at'
        ]
        read_only_fields = ['clinic_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True, 'min_length': 3},
            'email': {'required': True},
            'phone': {'required': True},
        }