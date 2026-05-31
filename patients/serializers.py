from rest_framework import serializers
from .models import Measurement, Patient, PatientInitialInfo

from appointments.serializers import AppointmentSerializer
from payments.serializers import PaymentSerializer
from  subscriptions.serializers import PlanSerializer
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'email', 'phone', 'gender', 'birth_date',
            'address', 'height', 'start_weight', 'profile_image',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PatientInitialInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInitialInfo
        fields = '__all__'

class PatientDetailSerializer(serializers.ModelSerializer):

    initial_info = PatientInitialInfoSerializer(read_only=True)
    measurements = MeasurementSerializer(many=True, read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    plans = PlanSerializer(many=True, read_only=True)

    packages = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    workshops = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'email',
            'phone',
            'gender',
            'birth_date',
            'address',
            'height',
            'start_weight',
            'profile_image',
            'created_at',
            'updated_at',

            'initial_info',
            'measurements',
            'appointments',
            'payments',
            'plans',

            'packages',
            'products',
            'workshops',
        ]
