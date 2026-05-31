from rest_framework import serializers 
from django.contrib.auth.hashers import make_password
from clinic.models import Patient

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = Patient 
        fields = ['name', 'email', 'password', 'confirmPassword']

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError({"password": "mismatch"})
        return data

    def create(self, validated_data):
        full_name = validated_data['name'].strip()
        parts = full_name.split(" ")

        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        validated_data.pop('confirmPassword')
        validated_data.pop('name')

        password = make_password(validated_data.pop('password'))

        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=validated_data['email'],
            password=password
        )

        return patient
