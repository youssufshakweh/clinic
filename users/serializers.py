from rest_framework import serializers 
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'birth_date', 'address', 'status', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified']


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone', 'gender', 'birth_date', 'address']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "كلمات المرور غير متطابقة"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.generate_otp()
        user.save()
        
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("البريد الالكتروني غير موجود")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    """التحقق من الرمز"""
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "البريد الالكتروني غير موجود"})
        
        if not user.verify_otp(data['otp']):
            raise serializers.ValidationError({"otp": "الرمز غير صحيح أو انتهت صلاحيته"})
        
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"password": "كلمات المرور غير متطابقة"})
        
        return data
    
    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.otp = None
        user.otp_created_at = None
        user.is_verified = True
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """تغيير كلمة المرور"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"password": "كلمات المرور الجديدة غير متطابقة"})
        return data


class SimpleRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("البريد الالكتروني مستخدم بالفعل")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.generate_otp()
        user.save()
        return user

